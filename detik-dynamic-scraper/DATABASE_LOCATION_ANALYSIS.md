# 📊 Database Location Analysis - Django vs FastAPI

**Issue:** Memastikan Django dan FastAPI menggunakan database yang sama

---

## 🔍 STRUKTUR DATABASE DI VPS:

Berdasarkan ls output VPS:

```
/root/suaranusa/
├── db.sqlite3                                    ❓ Django database?
├── detik-dynamic-scraper/
│   ├── data/
│   │   └── comprehensive_full_test.db           ✅ Main database (948 articles)
│   └── src/
│       └── data/
│           └── comprehensive_full_test.db       ✅ Same database (symlink/copy?)
```

---

## ⚠️ POTENTIAL ISSUE:

### **Django mungkin menggunakan db.sqlite3 yang berbeda!**

**Django default database:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # ❌ Beda database!
    }
}
```

**FastAPI database:**
```python
# src/api/main.py
DB_PATH = "data/comprehensive_full_test.db"  # ✅ Artikel ada di sini
```

**Result:**
- Django: Read from `db.sqlite3` (kosong/tidak ada artikel dari API)
- FastAPI: Read from `detik-dynamic-scraper/data/comprehensive_full_test.db` (948 articles)
- **Django TIDAK baca dari API, melainkan dari database lokal!**

---

## ✅ SOLUSI:

### **Cek di VPS (run ini):**

```bash
cd /root/suaranusa

# 1. Cek apakah Django punya database sendiri
ls -lh db.sqlite3

# 2. Cek isinya
sqlite3 db.sqlite3 ".tables"

# 3. Cek artikel di Django database
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM portal_article;" 2>/dev/null
# atau
sqlite3 db.sqlite3 "SELECT COUNT(*) FROM articles;" 2>/dev/null

# 4. Check Django models
cat portal/models.py | grep "class.*Model"
```

---

## 🎯 DUA KEMUNGKINAN:

### **Kemungkinan 1: Django Pakai DB Sendiri (Bukan API)**

Django mungkin punya model Article sendiri dan menyimpan di `db.sqlite3`:

```python
# portal/models.py
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.CharField(max_length=100)
    # ...
```

**Jika ini masalahnya:**
- Django tidak fetch dari API
- Django read dari database lokal (`db.sqlite3`)
- Database lokal kosong/tidak ter-update
- **Solusi:** Sync data dari FastAPI ke Django database

---

### **Kemungkinan 2: Django Fetch dari API (Tapi Gagal)**

Django fetch artikel via API tapi gagal karena config:

```python
# portal/views/home.py
api_service = ApiService()
articles = await api_service.get_articles()  # ❌ Fails karena wrong URL
```

**Jika ini masalahnya:**
- Django coba fetch dari API
- API_BASE_URL salah (localhost vs 127.0.0.1)
- Connection failed
- Empty article list
- **Solusi:** Fix API_BASE_URL di ecosystem.config.js

---

## 🔧 DEBUGGING STEPS (RUN DI VPS):

### **Step 1: Identifikasi Arsitektur**

```bash
cd /root/suaranusa

# Check Django models
cat portal/models.py | grep -A 10 "class Article"

# Check Django views
cat portal/views/home.py | grep -i "api\|article" | head -20
```

**Jika ada model Article:** Django pakai DB sendiri  
**Jika pakai ApiService:** Django fetch dari API

---

### **Step 2: Cek Django Database**

```bash
# Check if Django has local articles table
sqlite3 db.sqlite3 ".schema" | grep -i article

# Count articles in Django DB
sqlite3 db.sqlite3 "SELECT name FROM sqlite_master WHERE type='table';"
```

---

### **Step 3: Test API Connection dari Django**

```bash
# Django shell
source venv_detik/bin/activate
python manage.py shell

# In shell:
from django.conf import settings
print(f"API_BASE_URL: {settings.API_BASE_URL}")

# Test if Django fetches from API
from portal.services.api_client import ApiService
import asyncio

async def test():
    api = ApiService()
    try:
        articles = await api.get_articles(limit=5)
        print(f"✅ Fetched {len(articles)} articles from API")
        if articles:
            print(f"First: {articles[0]['title'][:60]}")
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(test())
```

---

## 📋 ARCHITECTURE POSSIBILITIES:

### **Architecture A: Django Direct DB (Not Using API)**

```
┌─────────────┐     Read      ┌──────────────┐
│   Django    │ ──────────> │  db.sqlite3  │
│   Portal    │               │ (Empty/Old)  │
└─────────────┘               └──────────────┘

┌─────────────┐     Read      ┌──────────────────────────┐
│   FastAPI   │ ──────────> │ detik-scraper/data/      │
│             │               │ comprehensive_full_test.db│
└─────────────┘               │ (948 articles)           │
                              └──────────────────────────┘

Problem: Django tidak baca dari FastAPI database!
Solution: Migrate to API-based architecture atau sync databases
```

---

### **Architecture B: Django Fetch from API (Current)**

```
┌─────────────┐   API Call   ┌─────────────┐
│   Django    │ ───────────> │   FastAPI   │
│   Portal    │   (Failed?)  │   :65080    │
└─────────────┘               └──────┬──────┘
                                     │
                                     ▼
                              ┌──────────────────┐
                              │ comprehensive_   │
                              │ full_test.db     │
                              │ (948 articles)   │
                              └──────────────────┘

Problem: API_BASE_URL mismatch (localhost vs 127.0.0.1)
Solution: Fix ecosystem.config.js
```

---

## ✅ VERIFICATION COMMANDS:

### **Run di VPS untuk identify architecture:**

```bash
# 1. Check Django architecture
cd /root/suaranusa
grep -r "ApiService\|api_client" portal/ --include="*.py"

# If found: Architecture B (API-based)
# If not found: Architecture A (Direct DB)

# 2. Check if Django has Article model
grep -r "class Article" portal/models.py

# If found: Django stores articles locally
# If not found: Django fetches from API only

# 3. Check Django views for API calls
cat portal/views/home.py | head -50
```

---

## 🎯 FINAL RECOMMENDATIONS:

### **If Architecture A (Direct DB):**

Django doesn't use FastAPI - it has its own database.

**Options:**
1. Migrate to API-based architecture (recommended)
2. Create sync script to copy data from FastAPI DB to Django DB
3. Point Django to use FastAPI database directly

**Quick Fix:**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'detik-dynamic-scraper/data/comprehensive_full_test.db',
    }
}
```

---

### **If Architecture B (API-based):**

Django fetches from API but connection fails.

**Fix:** Update ecosystem.config.js
```javascript
env: {
  API_BASE_URL: "http://127.0.0.1:65080"  // Not localhost!
}
```

Then restart:
```bash
pm2 restart suaranusa-portal
```

---

## 📝 NEXT STEPS:

1. **Identify architecture** - Run debugging commands above
2. **Verify database location** - Check which DB Django uses
3. **Test API connection** - If API-based, test connection
4. **Apply appropriate fix** - Based on architecture found

---

**Status:** Waiting for VPS debugging output  
**Likely Issue:** API_BASE_URL mismatch (localhost → 127.0.0.1)  
**Quick Fix:** Update ecosystem.config.js and restart PM2
