# 📑 Detik.com API Scraper - Complete Package Index

## 📚 Daftar File & Fungsinya

### 🎯 Start Here
1. **[README_DETIK_SCRAPER.md](README_DETIK_SCRAPER.md)** - Overview dan penjelasan project
2. **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Panduan cepat mulai menggunakan

### 📖 Dokumentasi
3. **[DETIK_API_FLOW_DOCUMENTATION.md](DETIK_API_FLOW_DOCUMENTATION.md)** - Dokumentasi lengkap API flow, endpoints, dan schema

### 🐍 Scripts
4. **[detik_api_scraper_stdlib.py](detik_api_scraper_stdlib.py)** - Script utama (recommended - no dependencies)
5. **[detik_api_scraper.py](detik_api_scraper.py)** - Versi dengan requests library

### 📊 Data Output
6. **[detik_comprehensive_data.json](detik_comprehensive_data.json)** - Data lengkap 573 artikel (284KB)
7. **[detik_article_ids.txt](detik_article_ids.txt)** - List 435 unique article IDs
8. **[detik_scraping_summary.txt](detik_scraping_summary.txt)** - Ringkasan hasil scraping

### 📝 Reference Files (Original)
9. **[htmlhome.md](htmlhome.md)** - HTML source dari detik.com homepage
10. **[fetchatauxhr.md](fetchatauxhr.md)** - XHR requests yang terdeteksi
11. **[scrape_home.py](scrape_home.py)** - Script scraping HTML awal
12. **[scraped_home.json](scraped_home.json)** - Hasil scraping HTML

---

## 🚀 Recommended Reading Order

### Untuk Quick Start:
```
1. README_DETIK_SCRAPER.md (overview)
   ↓
2. QUICK_START_GUIDE.md (cara pakai)
   ↓
3. Run: python3 detik_api_scraper_stdlib.py
   ↓
4. Explore: detik_comprehensive_data.json
```

### Untuk Understanding Flow:
```
1. fetchatauxhr.md (lihat XHR requests)
   ↓
2. DETIK_API_FLOW_DOCUMENTATION.md (pahami flow)
   ↓
3. detik_api_scraper_stdlib.py (lihat implementasi)
```

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| Total Articles | 573 |
| Unique IDs | 435 |
| API Endpoints | 4 |
| Channels | 12 |
| Scripts | 2 |
| Documentation Files | 4 |
| Data Files | 3 |

---

## 🎯 API Endpoints Summary

### 1. Recommendation API (Articles)
```
GET https://recg.detik.com/article-recommendation/wp/{id}?size={n}&nocache=1&ids=undefined&acctype=acc-detikcom
```
**Purpose:** Get recommended articles  
**Result:** 100 articles  

### 2. Recommendation20 API (Videos)
```
GET https://recg20.detik.com/article-recommendation/wp/{id}?size={n}
```
**Purpose:** Get video content  
**Result:** 50 videos  

### 3. Terpopuler Pages
```
GET https://www.detik.com/terpopuler
GET https://www.detik.com/terpopuler/{1|3|7|30}
```
**Purpose:** Get trending articles  
**Result:** 20 articles per timeframe  

### 4. Channel Homepages
```
GET https://{channel}.detik.com/
```
**Channels:** news, finance, sport, hot, inet, travel, food, health, wolipop, oto, edu  
**Result:** 15-59 articles per channel  

---

## 🔍 ID Patterns

### Article ID
- **Format:** `d-{8digits}`
- **Example:** `d-8412424`
- **URL Pattern:** `https://{channel}.detik.com/{category}/d-{id}/{slug}`

### Video ID
- **Format:** `{YYMMDD}{seq}`
- **Example:** `260323133` (23 Maret 2026, video ke-133)
- **URL Pattern:** `https://20.detik.com/{program}/{id}/{slug}`

---

## 💻 Usage Examples

### Python
```python
# Lihat QUICK_START_GUIDE.md untuk contoh lengkap
import urllib.request, json

url = "https://recg.detik.com/article-recommendation/wp/test?size=10&nocache=1&ids=undefined&acctype=acc-detikcom"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req).read())
```

### Bash/Curl
```bash
# Ambil 5 artikel
curl -s 'https://recg.detik.com/article-recommendation/wp/test?size=5&nocache=1&ids=undefined&acctype=acc-detikcom' | jq '.body[].title'

# Ambil 3 video
curl -s 'https://recg20.detik.com/article-recommendation/wp/test?size=3' | jq '.body[] | {id, title, duration}'
```

---

## ✅ Verification Status

- [x] API Endpoints discovered
- [x] ID patterns identified
- [x] Scripts tested and working
- [x] Data collected (573 articles)
- [x] Documentation complete
- [x] Live API tests verified

---

## 📅 Project Info

- **Created:** 2026-03-23
- **Total Articles Scraped:** 573
- **Unique IDs:** 435
- **Coverage:** Complete ✓
- **Status:** Production Ready

---

## 🎓 Next Steps

1. **Explore Data:**
   ```bash
   cat detik_comprehensive_data.json | jq '.statistics'
   ```

2. **Run Scraper:**
   ```bash
   python3 detik_api_scraper_stdlib.py
   ```

3. **Read Full Docs:**
   Open `DETIK_API_FLOW_DOCUMENTATION.md`

4. **Test Live API:**
   See examples in `QUICK_START_GUIDE.md`

---

**🎉 Everything is ready to use!**

For questions or issues, refer to the documentation files above.
