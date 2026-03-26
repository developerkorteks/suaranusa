# 🔧 VPS Django Fix - "NO DATA FOUND"

**Date:** 2026-03-26  
**Issue:** Django menampilkan "NO DATA FOUND" meskipun API punya data  
**Root Cause:** MISMATCH konfigurasi antara .env dan ecosystem.config.js

---

## 🔍 MASALAH DITEMUKAN!

### **Konflik Konfigurasi:**

**File: `.env`**
```bash
API_BASE_URL=http://127.0.0.1:65080  ✅ BENAR
```

**File: `ecosystem.config.js` (PM2)**
```javascript
env: {
  API_BASE_URL: "http://localhost:65080"  ❌ SALAH!
}
```

**Problem:**
- Django menggunakan `ecosystem.config.js` → API_BASE_URL = "http://localhost:65080"
- Tapi `localhost` kadang tidak resolve ke 127.0.0.1
- Django tidak bisa connect ke FastAPI
- Result: "NO DATA FOUND"

---

## 🔧 SOLUSI (Run di VPS):

### **Step 1: Update ecosystem.config.js**

```bash
cd /root/suaranusa
nano ecosystem.config.js
```

**Find this section:**
```javascript
{
  name: "suaranusa-portal",
  script: "./venv_detik/bin/python",
  args: "manage.py runserver 127.0.0.1:65081 --noreload",
  cwd: ".",
  interpreter: "none",
  env: {
    API_BASE_URL: "http://localhost:65080"  // ❌ GANTI INI
  }
},
```

**Change to:**
```javascript
{
  name: "suaranusa-portal",
  script: "./venv_detik/bin/python",
  args: "manage.py runserver 127.0.0.1:65081 --noreload",
  cwd: ".",
  interpreter: "none",
  env: {
    API_BASE_URL: "http://127.0.0.1:65080"  // ✅ GUNAKAN 127.0.0.1
  }
},
```

**Save:** Ctrl+O, Enter, Ctrl+X

---

### **Step 2: Restart PM2 Services**

```bash
# Restart Django portal
pm2 restart suaranusa-portal

# Check status
pm2 list

# View logs
pm2 logs suaranusa-portal --lines 50
```

---

### **Step 3: Verify Fix**

```bash
# Test API
curl http://127.0.0.1:65080/api/articles/search -X POST \
  -H "Content-Type: application/json" \
  -d '{"limit": 5}'

# Should return articles ✅

# Test Django
curl http://127.0.0.1:65081/

# Should return HTML with articles ✅
```

---

### **Step 4: Clear Browser Cache**

```
Chrome: Ctrl + Shift + R
Firefox: Ctrl + F5
```

---

## 📊 VERIFICATION:

### **Check PM2 Logs:**
```bash
# Real-time logs
pm2 logs suaranusa-portal

# Look for:
# - API connection errors (should be GONE)
# - "Fetched X articles" (should see this)
# - No timeout errors
```

### **Test Homepage:**
```bash
curl http://127.0.0.1:65081/ | grep -i "berita\|article"
```

### **Check From Browser:**
```
http://your-vps-ip:65081/
```

Should now show articles!

---

## 🎯 WHY THIS FIXES IT:

### **Before:**
```
Django PM2 Config:
  API_BASE_URL: "http://localhost:65080"

Django tries to connect:
  http://localhost:65080/api/articles/search
  → Sometimes fails to resolve
  → Connection refused
  → Empty article list
  → "NO DATA FOUND"
```

### **After:**
```
Django PM2 Config:
  API_BASE_URL: "http://127.0.0.1:65080"

Django connects:
  http://127.0.0.1:65080/api/articles/search
  → Always resolves correctly
  → Connection successful
  → Returns articles
  → Shows data! ✅
```

---

## 🔍 ADDITIONAL CHECKS:

### **If Still "NO DATA FOUND":**

1. **Check API is running:**
   ```bash
   curl http://127.0.0.1:65080/health
   # Should return: {"status":"healthy","database":"connected"}
   ```

2. **Check Django can reach API:**
   ```bash
   # Django shell
   pm2 stop suaranusa-portal
   cd /root/suaranusa
   source venv_detik/bin/activate
   python manage.py shell
   
   # In shell:
   from django.conf import settings
   print(settings.API_BASE_URL)  # Should be http://127.0.0.1:65080
   
   import httpx
   r = httpx.get(f"{settings.API_BASE_URL}/health")
   print(r.status_code)  # Should be 200
   print(r.json())  # Should show healthy status
   ```

3. **Test ApiService:**
   ```python
   # Still in Django shell
   from portal.services.api_client import ApiService
   import asyncio
   
   async def test():
       api = ApiService()
       articles = await api.get_articles(limit=5)
       print(f"Fetched {len(articles)} articles")
       for a in articles[:3]:
           print(f"  - {a['title'][:60]}")
   
   asyncio.run(test())
   # Should fetch and print articles
   ```

4. **Check PM2 Environment:**
   ```bash
   pm2 show suaranusa-portal
   # Look at "env" section
   # API_BASE_URL should be http://127.0.0.1:65080
   ```

---

## 📝 CURRENT VPS SETUP:

**Ports:**
- FastAPI: 65080
- Django: 65081

**PM2 Apps:**
- suaranusa-api (FastAPI)
- suaranusa-portal (Django)
- suaranusa-scheduler

**Database:**
- Location: detik-dynamic-scraper/data/comprehensive_full_test.db
- Articles: 1009
- Sources: 19 domains
- Quality: 100% (0 NULL)

---

## ✅ EXPECTED RESULT:

After fix, homepage should show:
- ✅ Latest articles from all sources
- ✅ Categories: NASIONAL, EKONOMI, OLAHRAGA, etc
- ✅ Pagination working
- ✅ Search working
- ✅ Filter by category working
- ✅ NO MORE "NO DATA FOUND"

Sample articles that should appear:
1. Arab Saudi Sebut Gangguan Iran di Selat Hormuz...
2. Parkir Liar di Sekitar Monas...
3. Harga Emas Antam Tak Bergerak...
4. Safari Lebaran Didit Prabowo...
5. Saham Garuda Tiba-tiba Terbang...
6. ... and 1004 more articles!

---

## 🎉 SUMMARY:

**Problem:** `localhost` vs `127.0.0.1` mismatch  
**Solution:** Update ecosystem.config.js to use `127.0.0.1`  
**Impact:** Django can now connect to API  
**Result:** Articles will display! 🚀

---

**Run on VPS:**
```bash
# 1. Edit config
nano /root/suaranusa/ecosystem.config.js
# Change localhost to 127.0.0.1

# 2. Restart
pm2 restart suaranusa-portal

# 3. Test
curl http://127.0.0.1:65081/ | grep -i berita

# 4. Browse
# Open browser to your VPS IP:65081
```

**Status:** ✅ Fix identified and ready to apply!
