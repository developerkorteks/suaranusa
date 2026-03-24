# 🚀 API EXAMPLES - Cara Pakai yang Benar

**Last Updated:** 24 March 2026 14:37

---

## ✅ QUICK START EXAMPLES

### **Example 1: Scrape Homepage (Paling Simple)**

```bash
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "news.detik.com",
    "save_to_db": false
  }'
```

**Response:**
```json
{
  "success": true,
  "articles_count": 20,
  "articles": [
    {
      "id": "8413316",
      "title": "Kapolri Monitoring Tempat Wisata...",
      "url": "https://news.detik.com/berita/d-8413316/...",
      ...
    }
  ],
  "timestamp": "2026-03-24T07:37:00"
}
```

---

### **Example 2: Scrape & Save ke Database**

```bash
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://wolipop.detik.com",
    "response_type": "html",
    "normalize": true,
    "save_to_db": true
  }'
```

**What happens:**
1. Scrape wolipop.detik.com
2. Normalize data (quality scoring, cleaning)
3. Save to database
4. Return results

---

### **Example 3: Get Statistics**

```bash
curl http://localhost:8000/api/statistics
```

**Response:**
```json
{
  "success": true,
  "database": {
    "total_articles": 558,
    "by_source": {
      "news.detik.com": 56,
      "wolipop.detik.com": 45,
      ...
    },
    "average_quality_score": 0.49
  }
}
```

---

### **Example 4: Search Articles**

```bash
curl -X POST "http://localhost:8000/api/articles/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Kapolri",
    "limit": 5
  }'
```

---

### **Example 5: Get Specific Article**

```bash
curl http://localhost:8000/api/articles/8413316
```

---

## 🎯 SWAGGER UI (Cara Termudah!)

Buka browser: **http://localhost:8000/docs**

**Kelebihan:**
- ✅ Interactive testing
- ✅ No need curl commands
- ✅ Auto-complete
- ✅ See all parameters
- ✅ Copy response

**Cara Pakai:**
1. Buka http://localhost:8000/docs
2. Pilih endpoint (e.g., POST /api/scrape)
3. Klik "Try it out"
4. Edit request body
5. Klik "Execute"
6. Lihat response!

---

## 📊 PARAMETER EXPLANATION

### **For /api/scrape:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | URL detik.com (bisa tanpa https://) |
| `response_type` | string | "auto" | "auto", "json", atau "html" |
| `normalize` | boolean | true | Normalize & clean data |
| `save_to_db` | boolean | true | Save to database |

### **Response Type:**
- `"auto"`: Auto-detect (recommended)
- `"html"`: Force HTML scraping
- `"json"`: Force JSON API

---

## ⚡ TIPS & TRICKS

### **1. Testing Mode (Fast)**
```json
{
  "url": "news.detik.com",
  "save_to_db": false  // ← Don't save (faster)
}
```

### **2. Production Mode (Save)**
```json
{
  "url": "news.detik.com",
  "save_to_db": true   // ← Save to DB
}
```

### **3. URL Formats (All work!)**
```json
{"url": "news.detik.com"}                    // ✅ OK
{"url": "https://news.detik.com"}            // ✅ OK
{"url": "https://news.detik.com/indeks"}     // ✅ OK
```

---

## 🐛 COMMON ERRORS & FIXES

### ❌ Error: "URL cannot be empty"
```json
{"url": ""}  // Wrong!
{"url": "news.detik.com"}  // ✅ Fixed!
```

### ❌ Error: "Only detik.com domains allowed"
```json
{"url": "google.com"}  // Wrong! (security)
{"url": "news.detik.com"}  // ✅ Fixed!
```

### ❌ Error: "response_type must be..."
```json
{"response_type": "xml"}  // Wrong!
{"response_type": "html"}  // ✅ Fixed!
```

---

## 🎯 COMPLETE WORKFLOW EXAMPLE

```bash
# 1. Scrape articles
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{"url":"news.detik.com","save_to_db":true}'

# 2. Check statistics
curl http://localhost:8000/api/statistics

# 3. Get articles
curl "http://localhost:8000/api/articles?limit=5"

# 4. Search specific topic
curl -X POST "http://localhost:8000/api/articles/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"politik","limit":10}'

# 5. Export to JSON
curl -X POST "http://localhost:8000/api/export?limit=100"
```

---

**API Fixed:** ✅  
**Ready to Use:** ✅  
**Documentation:** ✅ Complete
