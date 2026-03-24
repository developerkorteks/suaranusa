# Perencanaan Arsitektur Django Frontend: News Portal Engine (Phase 1)

## 1. Pendahuluan
Dokumen ini menetapkan standar teknis dan strategi implementasi untuk membangun portal berita menggunakan Django 4.2.3 yang mengonsumsi Detik Scraper API. Fokus utama adalah menciptakan sistem yang sepenuhnya dinamis, otomatis (zero-button), dan memiliki performa tinggi setara dengan portal berita produksi nasional.

## 2. Arsitektur Sistem (Two-Tier Architecture)
Sistem akan beroperasi dengan memisahkan fungsi secara tegas:
*   **Backend Layer (FastAPI):** Bertanggung jawab atas scraping, persistensi data (SQLite), dan logika ekstraksi konten.
*   **Frontend Layer (Django):** Bertanggung jawab atas manajemen sesi user, caching, rendering UI, dan orkestrasi konsumsi API.

---

## 3. Strategi Aliran Data & Automasi (Zero Button Interaction)

### A. Strategi Pemuatan Halaman Utama (Home Feed)
*   **Pola Fetch-and-Sync:** Saat `HomePageView` diakses, Django akan melakukan request `GET /api/articles/search`.
*   **Trigger Latar Belakang (Passive Trigger):** Django akan menyimpan timestamp terakhir sinkronisasi di cache. Jika sudah melewati ambang batas (contoh: 15 menit), Django akan secara otomatis mengirimkan request `POST /api/scrape` ke FastAPI di latar belakang (background task) tanpa menunda rendering halaman ke user.

### B. Strategi Detailing & Pengayaan (Content Enrichment)
*   **Lazy Loading Content:** Saat user mengklik artikel, Django memanggil `GET /api/articles/{id}`.
*   **Auto-Scrape Logic:** Jika field `content` dalam database API bernilai kosong, Django akan secara otomatis memicu `POST /api/articles/{id}/scrape-detail`. Proses ini dilakukan sekali, dan user akan melihat transisi mulus dari *Skeleton Screen* ke konten penuh.

---

## 4. Struktur Proyek Django (Proposed Organization)

```text
django_news_portal/
├── core/                   # Django Project Configuration
│   ├── settings.py         # Config API Base URL, Cache, Database
│   └── urls.py             # Main Route mapping
├── portal/                 # News Portal Application
│   ├── services/           # Logika Konsumsi API (api_client.py)
│   ├── utils/              # Helper Formatting Tanggal & Teks
│   ├── views/              # Class Based Views (Home, Category, Detail)
│   ├── urls.py             # App Route mapping
│   └── models.py           # (Minimal - Database API as Single Source)
├── templates/
│   ├── base.html           # Struktur HTML5 (SEO Optimized)
│   ├── components/         # Navbar, Footer, Sidebar, Card News
│   ├── news/
│   │   ├── home.html       # Headline + Grid Section
│   │   ├── category.html   # Filtered List by Source
│   │   └── detail.html     # Full Article View with Clean Typography
└── static/                 # CSS (Tailwind), JS, Images
```

---

## 5. API Service Layer (The Bridge)
Django tidak akan menggunakan ORM tradisional untuk artikel. Sebaliknya, sebuah `ApiService` akan dibangun menggunakan library `httpx` untuk mendukung operasi asinkron:

*   **Singleton Pattern:** Memastikan hanya ada satu instance koneksi API.
*   **Error Resilience:** Jika API Backend down, Django akan menampilkan halaman "Maintenance" yang elegan atau memuat data dari cache terakhir yang tersedia.
*   **Response Mapping:** Mengonversi JSON dari API menjadi objek Python agar mudah diakses di template (`article.title` vs `article['title']`).

---

## 6. Desain UI/UX & Typography
*   **Framework:** Tailwind CSS (v3.x).
*   **Layout:** Responsive Mobile-First (Grid System).
*   **Typography:** Menggunakan font Sans-Serif yang bersih (misal: Inter atau Roboto) dengan fokus pada keterbacaan artikel (Reading Mode).
*   **Interactive Feedback:** Shimmer/Skeleton effect saat konten sedang di-scrape di latar belakang.

---

## 7. Tahapan Implementasi (Roadmap)

### Tahap 1: Inisialisasi Project (Setup Environment)
*   Instalasi Django 4.2.3, `httpx`, dan `python-dotenv`.
*   Konfigurasi `settings.py` untuk mengarah ke API Backend (FastAPI).

### Tahap 2: Pembangunan Service Layer
*   Implementasi `api_client.py` untuk fungsi `fetch_articles()`, `get_article_detail()`, dan `trigger_scrape()`.

### Tahap 3: Pengembangan Template & View
*   Pembuatan `BaseView` dan `HomePageView`.
*   Setup Tailwind CSS dan komponen berita (Card, Badge, Pagination).

### Tahap 4: Logika Automasi (Detail Scrape)
*   Implementasi pengecekan konten otomatis pada `ArticleDetailView`.
*   Integrasi status loading yang halus.

### Tahap 5: Optimasi & Caching
*   Implementasi Django Cache untuk mengurangi beban ke API Backend.
*   Minifikasi aset statis (CSS/JS).

---

## 8. Analisis Risiko & Mitigasi
*   **Risiko:** Waktu tunggu (latency) API Backend tinggi.
*   **Mitigasi:** Gunakan caching agresif (1-5 menit) untuk halaman depan dan simpan data artikel detail di cache selama 24 jam setelah sukses di-scrape.
