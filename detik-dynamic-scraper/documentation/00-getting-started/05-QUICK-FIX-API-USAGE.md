# 🔧 QUICK FIX GUIDE - API Usage

**Last Updated:** 24 March 2026 14:36

---

## ❌ MASALAH YANG DITEMUKAN

### **1. URL Validation Error**
```
Error: "URL cannot be empty or None, got: HttpUrl"
```

**Penyebab:** Pydantic HttpUrl type terlalu ketat untuk validator

**Fix:** ✅ Changed from `HttpUrl` to `str` with manual validation

---

### **2. SLOW REQUEST Warnings**
```
WARNING: SLOW REQUEST: POST /api/discover-domains took 22.84s
WARNING: SLOW REQUEST: POST /api/detect-endpoints took 12.41s
```

**Penyebab:** Normal behavior - ini operasi yang memang lama:
- Domain discovery: Scrape homepage untuk find all subdomains
- Endpoint detection: Parse 50+ script tags dengan regex

**Solusi:**
- ✅ Already has caching
- ✅ Logged as WARNING (informational)
- ⚡ Optimization available in Sprint 3

---

### **3. /page Endpoint Not Found (404)**
```
GET /page: 404 Not Found
```

**Penyebab:** Endpoint ini untuk serve static HTML samples

**Fix:** Not needed for API usage, hanya untuk development testing

---

## ✅ CARA PAKAI API YANG BENAR

### **1. Scrape URL (Simplest)**

```bash
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "news.detik.com",
    "response_type": "html",
    "save_to_db": false
  }'
```

**Notes:**
- URL bisa tanpa `https://` (auto-added)
- `response_type`: `auto`, `json`, atau `html`
- `save_to_db`: `false` untuk testing (tidak save ke DB)

---

### **2. Discover Domains**

```bash
curl -X POST "http://localhost:8000/api/discover-domains" \
  -H "Content-Type: application/json" \
  -d '{
    "base_url": "https://www.detik.com"
  }'
```

**Expected:** ~20-25 seconds (normal)  
**Returns:** List of discovered subdomains

---

### **3. Detect Endpoints**

```bash
curl -X POST "http://localhost:8000/api/detect-endpoints" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "news.detik.com"
  }'
```

**Expected:** ~10-15 seconds (normal)  
**Returns:** List of API endpoints

---

### **4. Get Articles**

```bash
curl -X GET "http://localhost:8000/api/articles?limit=10"
```

**Returns:** List of articles from database

---

### **5. Get Statistics**

```bash
curl -X GET "http://localhost:8000/api/statistics"
```

**Returns:** Database statistics

---

## 🎯 CONTOH PENGGUNAAN LENGKAP

### **Scenario 1: Quick Test Scraping**

```bash
# 1. Scrape homepage (cepat, tidak save)
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "news.detik.com",
    "response_type": "html",
    "save_to_db": false
  }' | jq .

# 2. Check hasilnya
# Akan return JSON dengan articles array
```

---

### **Scenario 2: Production Scraping & Save**

```bash
# 1. Scrape dan save ke database
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.detik.com/indeks",
    "response_type": "html",
    "normalize": true,
    "save_to_db": true
  }' | jq .

# 2. Check statistics
curl -X GET "http://localhost:8000/api/statistics" | jq .

# 3. Get articles
curl -X GET "http://localhost:8000/api/articles?limit=5" | jq .
```

---

### **Scenario 3: Full Discovery Flow**

```bash
# 1. Discover all domains (~25s)
curl -X POST "http://localhost:8000/api/discover-domains" \
  -H "Content-Type: application/json" \
  -d '{"base_url": "https://www.detik.com"}' | jq .

# 2. Detect endpoints for specific domain (~12s)
curl -X POST "http://localhost:8000/api/detect-endpoints" \
  -H "Content-Type: application/json" \
  -d '{"domain": "news.detik.com"}' | jq .

# 3. Scrape using detected info
curl -X POST "http://localhost:8000/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.detik.com/indeks",
    "save_to_db": true
  }' | jq .
```

---

## 📊 EXPECTED PERFORMANCE

```
Endpoint                    Expected Time    Normal?
─────────────────────────────────────────────────────
/api/scrape                 1-5s            ✅
/api/discover-domains       20-25s          ✅ (cached after)
/api/detect-endpoints       10-15s          ✅ (cached after)
/api/articles               <1s             ✅
/api/statistics             <1s             ✅
```

---

## ⚡ OPTIMIZATION TIPS

### **1. Use Caching**
- Domain discovery & endpoint detection di-cache
- Second call will be instant

### **2. Scrape Efficiently**
```json
{
  "url": "news.detik.com",
  "response_type": "html",    // Specify type (faster)
  "save_to_db": false         // Test mode (faster)
}
```

### **3. Batch Operations**
- Scrape multiple pages → use `/api/scrape` multiple times
- Results auto-saved to database

---

## 🐛 TROUBLESHOOTING

### **Error: "URL cannot be empty"**
**Fix:** Pastikan URL tidak kosong
```json
{"url": "news.detik.com"}  // ✅ OK
{"url": ""}                 // ❌ Error
```

### **Error: "Only detik.com domains allowed"**
**Fix:** Hanya bisa scrape detik.com
```json
{"url": "news.detik.com"}   // ✅ OK
{"url": "google.com"}        // ❌ Error (security)
```

### **Error: "response_type must be..."**
**Fix:** Gunakan: auto, json, atau html
```json
{"response_type": "html"}   // ✅ OK
{"response_type": "xml"}    // ❌ Error
```

### **SLOW REQUEST Warning**
**Normal!** Discovery & detection memang lama (10-25s)
- Di-cache setelah call pertama
- Call kedua akan instant

---

## 📖 SWAGGER UI

Buka browser: `http://localhost:8000/docs`

**Benefits:**
- Interactive API testing
- Auto-generated documentation
- Try out all endpoints
- See request/response schemas

---

## 🎯 QUICK REFERENCE

```bash
# Health check
curl http://localhost:8000/health

# Scrape (simple)
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"news.detik.com","save_to_db":false}'

# Get articles
curl http://localhost:8000/api/articles?limit=5

# Statistics
curl http://localhost:8000/api/statistics

# Export
curl -X POST http://localhost:8000/api/export?limit=10
```

---

**Fixed Issues:** ✅  
**API Working:** ✅  
**Documentation:** ✅ Complete  

Happy scraping! 🚀
