# Quick Start Guide - Detik.com API Scraper

## 🚀 Cara Cepat Menggunakan

### 1. Jalankan Script Utama
```bash
python3 detik_api_scraper_stdlib.py
```

Output:
- `detik_comprehensive_data.json` - Data lengkap (284KB)
- `detik_article_ids.txt` - 435 unique IDs
- `detik_scraping_summary.txt` - Ringkasan

### 2. Test API Langsung dengan Curl

#### Ambil 10 Artikel Terbaru
```bash
curl -s 'https://recg.detik.com/article-recommendation/wp/test?size=10&nocache=1&ids=undefined&acctype=acc-detikcom' \
  -H 'User-Agent: Mozilla/5.0' | jq '.body[] | {id, title, url: .articleurl}'
```

#### Ambil 5 Video Terbaru
```bash
curl -s 'https://recg20.detik.com/article-recommendation/wp/test?size=5' \
  -H 'User-Agent: Mozilla/5.0' | jq '.body[] | {id, title, duration, videourl}'
```

#### Lihat Artikel Trending 7 Hari
```bash
curl -s 'https://www.detik.com/terpopuler/7' | grep -oP '/d-\d+/' | sort -u
```

### 3. Contoh Python Sederhana

```python
import urllib.request
import json

# Ambil 20 artikel
url = "https://recg.detik.com/article-recommendation/wp/test?size=20&nocache=1&ids=undefined&acctype=acc-detikcom"
headers = {'User-Agent': 'Mozilla/5.0'}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode('utf-8'))
    
for article in data['body']:
    print(f"{article['id']} - {article['title']}")
```

### 4. Explore Data JSON

```bash
# Lihat statistik
cat detik_comprehensive_data.json | jq '.statistics'

# Lihat artikel dari recommendation API
cat detik_comprehensive_data.json | jq '.sources.recommendation_api.articles[0:5]'

# Lihat video
cat detik_comprehensive_data.json | jq '.sources.recommendation20_api.articles[0:3]'

# Cari artikel berdasarkan keyword
cat detik_comprehensive_data.json | jq '.sources.recommendation_api.articles[] | select(.title | contains("Iran"))'
```

## 📊 Hasil yang Didapat

- ✅ **573 artikel** total
- ✅ **435 unique IDs**
- ✅ **100 artikel** dari Recommendation API
- ✅ **50 video** dari Recommendation20 API
- ✅ **323 artikel** dari berbagai channel

## 🔗 Endpoint Utama

| Endpoint | Purpose | Size Param | Format |
|----------|---------|------------|--------|
| `recg.detik.com/article-recommendation/wp/{id}` | Articles | 1-100+ | JSON |
| `recg20.detik.com/article-recommendation/wp/{id}` | Videos | 1-100+ | JSON |
| `www.detik.com/terpopuler` | Trending All | - | HTML |
| `www.detik.com/terpopuler/{days}` | Trending Period | 1,3,7,30 | HTML |

## 📖 Dokumentasi Lengkap

Lihat `DETIK_API_FLOW_DOCUMENTATION.md` untuk:
- Detail semua endpoint
- Response schema
- Advanced usage
- Best practices
- Error handling

## ⚡ Tips

1. **Rate Limiting**: Gunakan delay 1-2 detik antar request
2. **User Agent**: Selalu set User-Agent header
3. **Error Handling**: Implement try-catch untuk production
4. **Caching**: Simpan hasil untuk mengurangi request

## 🎯 Use Cases

- Content aggregation
- Trending analysis
- Video monitoring
- News archive
- Research & analytics

---

**Ready to use!** ✅ Semua script dan data sudah siap digunakan.
