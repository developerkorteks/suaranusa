# Panduan Integrasi API Detik Dynamic Scraper (Best Practice)

Dokumen ini menjelaskan strategi implementasi untuk membangun frontend berita yang sepenuhnya otomatis, modern, dan tanpa intervensi manual (zero-button interaction).

## 1. Arsitektur Komunikasi Data
Sistem menggunakan pola **Asynchronous Data Enrichment**. Frontend tidak hanya menampilkan data statis, tetapi juga secara cerdas memicu pembaruan konten di latar belakang.

### Endpoint Utama
| Method | Endpoint | Kegunaan |
| :--- | :--- | :--- |
| `POST` | `/api/articles/search` | Mengambil daftar artikel (Feed Utama). |
| `GET` | `/api/articles/{id}` | Mengambil data lengkap satu artikel. |
| `POST` | `/api/articles/{id}/scrape-detail` | Memicu ekstraksi konten artikel secara on-demand. |
| `POST` | `/api/scrape` | Memperbarui daftar artikel dari domain sumber. |

---

## 2. Strategi Implementasi Frontend Otomatis

### A. Alur Pemuatan Halaman Utama (Home/Feed)
Untuk menghadirkan pengalaman "Always Fresh", frontend harus melakukan sinkronisasi secara otomatis:

1.  **Initial Load:** Panggil `/api/articles/search` dengan parameter `limit` dan `source`.
2.  **Background Sync:** Di sisi server (Next.js/Node.js) atau via background worker, panggil `/api/scrape` secara berkala (misal: setiap 15 menit) untuk memastikan daftar berita selalu diperbarui tanpa menunggu aksi user.
3.  **Content Mapping:** Gunakan field `image` untuk kartu berita dan `quality_score` untuk menentukan artikel mana yang masuk ke bagian "Top News".

### B. Alur Pemuatan Detail Artikel (Single Page)
Saat user mengklik artikel, frontend harus menangani kondisi data yang belum lengkap secara elegan:

1.  **Pengecekan Konten:** Ambil data via `/api/articles/{id}`.
2.  **Auto-Enrichment Logic:**
    *   Jika field `content` bernilai `null` atau kosong:
        *   Tampilkan komponen *Skeleton Screen*.
        *   Secara otomatis panggil `/api/articles/{id}/scrape-detail` di latar belakang.
        *   Setelah sukses, perbarui state UI dengan konten yang baru saja diekstraksi.
    *   Jika field `content` sudah ada:
        *   Langsung tampilkan konten untuk performa instan.

### C. Strategi Media & Gambar
*   Gunakan field `image` dari metadata artikel.
*   Jika artikel memiliki video (detikTV / 20.detik.com), sistem akan mengembalikan URL video di dalam field `metadata` atau `videos` setelah proses `scrape-detail` selesai.

---

## 3. Best Practice Teknis

### Keamanan & Performa
1.  **Rate Limiting:** Pastikan frontend tidak melakukan request ke `/api/scrape` atau `/scrape-detail` secara berlebihan dalam satu waktu yang sama (Batching).
2.  **Caching:** Implementasikan caching di sisi frontend (misal: Redis atau SWR/React Query) untuk data `/api/articles/{id}` yang sudah lengkap guna mengurangi beban database.
3.  **Error Handling:** Selalu siapkan fallback UI jika proses scraping detail gagal (misal: tombol "Coba Lagi" atau link langsung ke sumber asli).

### Contoh Struktur Konsumsi (Pseudo-code)
```javascript
// Fungsi Otomatis untuk Detail Artikel
async function getArticleDetail(id) {
    let response = await fetch(`/api/articles/${id}`);
    let data = await response.json();
    
    // Jika konten belum ada, picu scraping otomatis
    if (!data.article.content) {
        await fetch(`/api/articles/${id}/scrape-detail`, { method: 'POST' });
        // Re-fetch data terbaru
        response = await fetch(`/api/articles/${id}`);
        data = await response.json();
    }
    
    return data.article;
}
```

---

## 4. Kesimpulan
Dengan mengikuti alur di atas, frontend akan berfungsi layaknya portal berita produksi besar yang selalu terbarui secara otomatis, memberikan pengalaman pengguna yang mulus tanpa perlu proses manual di sisi admin.
