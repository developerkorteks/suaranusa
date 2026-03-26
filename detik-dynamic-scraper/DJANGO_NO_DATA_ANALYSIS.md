# 🔍 Analisa: Django "NO DATA FOUND"

**Issue:** Django tidak menampilkan artikel meskipun API dan database working

---

## ✅ Yang Sudah Dicek:

1. **API Running:** ✅
   ```bash
   curl http://127.0.0.1:65080/health
   → {"status":"healthy","database":"connected"}
   ```

2. **Database Has Data:** ✅
   ```
   Total articles: 1009
   Sources: 19 domains
   NULL sources: 0
   ```

3. **API Returns Data:** ✅
   ```bash
   curl http://127.0.0.1:65080/api/articles/search
   → Returns articles successfully
   ```

4. **Source Field Working:** ✅
   ```json
   {
     "source": "news.detik.com",  // ✅ Correct format
     "source_url": "..."
   }
   ```

---

## ❌ Root Cause: Django Configuration

### **Problem #1: Django Not Running**
```bash
ps aux | grep manage.py
→ No Django process found!
```

**Django perlu di-start:**
```bash
cd /path/to/django/project
python manage.py runserver
```

---

### **Problem #2: API_BASE_URL Mismatch**

**Django expects:**
```python
# settings.py
API_BASE_URL = "http://localhost:8000"  ❌
```

**FastAPI running on:**
```
http://127.0.0.1:65080  ✅
```

**Fix:**
```python
# Update settings.py
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:65080")
```

---

### **Problem #3: Search Query**

**Issue:** Search "China Emas" tidak menemukan karena:
- Artikel title: "Jackpot! China Temukan Cadangan Emas..."
- Search exact: "China Emas" (tidak ada spasi "Temukan Cadangan")

**Test Search:**
```bash
# Search "China" → Found
curl -X POST http://127.0.0.1:65080/api/articles/search \
  -d '{"query": "China"}'

# Search "emas" → Found  
curl -X POST http://127.0.0.1:65080/api/articles/search \
  -d '{"query": "emas"}'
```

---

## 🔧 SOLUSI LENGKAP:

### **Step 1: Update Django Settings**

Lokasi VPS: `/root/suaranusa/core/settings.py`

```python
# Find and update:
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:65080")
```

### **Step 2: Start Django (if not running)**

```bash
cd /root/suaranusa
source venv_detik/bin/activate
python manage.py runserver 0.0.0.0:8000
```

### **Step 3: Clear Cache**

```python
# Django shell
from django.core.cache import cache
cache.clear()
```

### **Step 4: Verify Connection**

```python
# Django shell
from django.conf import settings
import httpx

# Test connection
response = httpx.get(f"{settings.API_BASE_URL}/health")
print(response.status_code)  # Should be 200
print(response.json())  # Should be {"status":"healthy"...}
```

### **Step 5: Test API Client**

```python
# Django shell
from portal.services.api_client import ApiService
import asyncio

async def test():
    api = ApiService()
    articles = await api.get_articles(limit=5)
    print(f"Fetched {len(articles)} articles")
    for a in articles[:3]:
        print(f"  - {a['title'][:60]}")
        print(f"    Source: {a.get('source', 'MISSING')}")

asyncio.run(test())
```

### **Step 6: Check Homepage**

```bash
# Access Django homepage
curl http://localhost:8000/

# Should return HTML with articles
```

---

## 📊 Test Pagination & Categories:

### **Test Homepage:**
```bash
curl http://localhost:8000/
# Should show latest articles
```

### **Test Category Filter:**
```bash
curl http://localhost:8000/?cat=NASIONAL
curl http://localhost:8000/?cat=EKONOMI
curl http://localhost:8000/?cat=OLAHRAGA
```

### **Test Pagination:**
```bash
curl http://localhost:8000/?page=1
curl http://localhost:8000/?page=2
curl http://localhost:8000/?page=3
```

### **Test Search:**
```bash
curl http://localhost:8000/?q=China
curl http://localhost:8000/?q=ekonomi
curl http://localhost:8000/?q=politik
```

---

## ✅ Expected Behavior:

**Homepage (/):**
- Should show 12 articles per page
- Categories from all sources
- Pagination links

**Category Filter (?cat=NASIONAL):**
- Show articles from news.detik.com
- Client-side filtering based on URL/source

**Search (?q=China):**
- API search for matching articles
- Return results with "China" in title/content

**Pagination (?page=2):**
- Show next 12 articles
- Has previous/next links

---

## 🐛 Debug Steps:

### **1. Check Django Logs:**
```bash
# Look for errors
tail -f /path/to/django/logs/*.log

# Common errors:
# - Connection refused (API not running)
# - Timeout (API slow)
# - 404 (Wrong endpoint)
```

### **2. Check API Response:**
```python
# Django view
def home(request):
    api_service = ApiService()
    articles = await api_service.get_articles(limit=12)
    print(f"DEBUG: Fetched {len(articles)} articles")  # Add this
    print(f"DEBUG: First article: {articles[0] if articles else 'NONE'}")
    # ...
```

### **3. Check Browser Console:**
```javascript
// Open browser developer tools
// Check Network tab for API calls
// Look for 404/500 errors
```

### **4. Test API Direct:**
```bash
# From VPS
curl http://127.0.0.1:65080/api/articles/search \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"limit": 5}'

# Should return 5 articles
```

---

## 📝 Common Issues:

### **Issue: "NO DATA FOUND"**

**Cause 1:** Django can't connect to API
```python
# Check settings.py
API_BASE_URL = "http://127.0.0.1:65080"  # Must match FastAPI port
```

**Cause 2:** API not running
```bash
# Start FastAPI
cd /root/suaranusa/detik-dynamic-scraper
source /root/suaranusa/venv_detik/bin/activate
python3 -m uvicorn src.api.main:app --port 65080 --host 0.0.0.0
```

**Cause 3:** Empty response from API
```python
# Check if ApiService.get_articles() returns empty list
# Add logging to see what's happening
```

**Cause 4:** Template rendering issue
```django
{# Check template #}
{% if articles %}
  {% for article in articles %}
    {{ article.title }}
  {% endfor %}
{% else %}
  <p>NO DATA FOUND</p>  {# This is showing #}
{% endif %}
```

---

## ✅ Final Checklist:

Before declaring "NO DATA FOUND" is fixed, verify:

- [ ] FastAPI running on port 65080
- [ ] Django running on port 8000
- [ ] API_BASE_URL correct in settings.py
- [ ] Can curl FastAPI successfully
- [ ] Can curl Django successfully
- [ ] ApiService can fetch articles
- [ ] Template receives article list
- [ ] Browser shows articles
- [ ] Categories work
- [ ] Pagination works
- [ ] Search works

---

**Status:** Waiting for Django configuration update
**Next:** Update API_BASE_URL and restart Django
