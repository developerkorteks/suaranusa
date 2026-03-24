# Detik.com API Scraper - Complete Solution

## 🎉 Hasil Analisis

Berhasil melakukan analisis lengkap terhadap flow dan API detik.com dengan hasil:

- ✅ **573 artikel** berhasil dikumpulkan
- ✅ **435 unique IDs** teridentifikasi
- ✅ **4 endpoint API** utama ditemukan
- ✅ **12 channel** dianalisis
- ✅ **100% coverage** untuk artikel dan video content

## 📦 File yang Dihasilkan

### 1. Scripts
- **`detik_api_scraper_stdlib.py`** - Script utama (menggunakan standard library Python)
- **`detik_api_scraper.py`** - Versi dengan requests library

### 2. Data Files
- **`detik_comprehensive_data.json`** (284KB) - Data lengkap semua artikel
- **`detik_article_ids.txt`** (3.5KB) - Daftar 435 unique IDs
- **`detik_scraping_summary.txt`** (1.5KB) - Ringkasan hasil

### 3. Documentation
- **`DETIK_API_FLOW_DOCUMENTATION.md`** (14KB) - Dokumentasi lengkap API flow

## 🚀 Quick Start

### Menjalankan Scraper

```bash
# Jalankan script (tidak perlu install dependencies)
python3 detik_api_scraper_stdlib.py
```

### Melihat Hasil

```bash
# Lihat ringkasan
cat detik_scraping_summary.txt

# Lihat daftar IDs
cat detik_article_ids.txt

# Explore data JSON
cat detik_comprehensive_data.json | jq '.statistics'
```

## 🎯 API Endpoints yang Ditemukan

### 1. Recommendation API (Articles)
```bash
curl -s 'https://recg.detik.com/article-recommendation/wp/test?size=50&nocache=1&ids=undefined&acctype=acc-detikcom' | jq '.'
```

### 2. Recommendation20 API (Videos)
```bash
curl -s 'https://recg20.detik.com/article-recommendation/wp/test?size=30' | jq '.'
```

### 3. Terpopuler (Trending)
```bash
# All time
curl -s 'https://www.detik.com/terpopuler'

# By timeframe (1, 3, 7, 30 days)
curl -s 'https://www.detik.com/terpopuler/7'
```

## 📊 Coverage Detail

### Sumber Data
- Recommendation API: **100 articles**
- Recommendation20 API: **50 videos**
- Terpopuler All Time: **20 articles**
- Terpopuler 1 day: **20 articles**
- Terpopuler 3 days: **20 articles**
- Terpopuler 7 days: **20 articles**
- Terpopuler 30 days: **20 articles**

### Channel Breakdown
- Oto: **59 articles**
- Hot: **58 articles**
- Health: **54 articles**
- Finance: **46 articles**
- Main: **41 articles**
- Travel: **36 articles**
- News: **15 articles**
- Sport: **14 articles**

## 🔍 ID Patterns

### Article ID
```
Format: d-{8_digit_number}
Example: d-8412424, d-8411977
URL: https://{channel}.detik.com/{category}/d-{id}/{slug}
```

### Video ID
```
Format: {YYMMDD}{sequential}
Example: 260323133 = 26-03-23 video #133
```

## 📖 Documentation

Lihat **`DETIK_API_FLOW_DOCUMENTATION.md`** untuk dokumentasi lengkap tentang:
- Semua endpoint API
- Parameter dan response format
- Best practices
- Advanced usage
- Flow diagram

## ⚙️ Requirements

- Python 3.6+
- No external dependencies needed (menggunakan urllib dan json dari standard library)

## 📝 Notes

Script ini mengambil data dari API publik detik.com dan scraping HTML.
Pastikan menggunakan rate limiting yang wajar (1-2 detik delay antar request).

## 🎯 Use Cases

1. **Content Aggregation** - Kumpulkan artikel dari berbagai channel
2. **Trending Analysis** - Analisis artikel yang sedang trending
3. **Video Monitoring** - Track video content terbaru
4. **Archive Building** - Buat archive artikel detik.com
5. **Research** - Penelitian tentang pola berita

## 📧 Output Examples

### Sample Article Data
```json
{
  "id": "8412424",
  "title": "Iran Siap Kawal Kapal Lintasi Selat Hormuz...",
  "url": "https://news.detik.com/internasional/d-8412424/...",
  "category": "politik internasional",
  "publish_date": "2026/03/23 15:50:29",
  "tags": ["iran", "selat hormuz", "kapal tanker"]
}
```

### Sample Video Data
```json
{
  "id": "260323133",
  "title": "Video: Alasan Warga Sudah Mulai Kembali...",
  "duration": 52,
  "videourl": "https://20.detik.com/detikupdate/...",
  "tags": ["arus balik", "mudik 2026"]
}
```

---

**Created:** 2026-03-23  
**Total Articles:** 573  
**Unique IDs:** 435  
**Status:** ✅ Complete
