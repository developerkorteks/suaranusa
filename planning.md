# 📜 Project Planning: Manual News Upload Feature (Hybrid Approach)

**Status:** 🏗️ Analysis & Planning Phase (DRAFT v1.0)  
**Objective:** Add a manual news upload feature to `suaranusa.my.id` using Django Admin, while maintaining seamless integration with the existing Scraper API.  
**Architecture:** Hybrid Data Source (Local Django DB + Remote FastAPI Scraper).

---

## 🔍 1. Current Workflow Analysis
- **Scraper Service:** Runs on FastAPI, saves to `scraper.db`, exposes `/api/articles`.
- **Frontend (Django):** Calls `/api/articles/search`, processes items on-the-fly, and renders them.
- **Limitation:** Currently, there is no way to add "original" content or "exclusive" news directly without going through the scraping process.

---

## 🛠️ 2. Proposed Technical Architecture (Option B: Hybrid)

### **A. Data Sovereignty**
- **Scraper Data:** Stays in the remote database (FastAPI).
- **Manual Data:** Stays in the local Django database (`db.sqlite3`).
- **Why?** Better media handling (Django's `ImageField`/`FileField` is robust), native Admin integration, and zero overhead for the scraper system.

### **B. New Data Model (`portal/models.py`)**
A new model `ManualArticle` will be created with fields matching the Scraper's output schema to ensure template compatibility.

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | News headline. |
| `slug` | SlugField | URL-friendly title (auto-generated). |
| `main_image` | ImageField | Featured image (stored in `/media/manual_news/`). |
| `category` | CharField | Matches existing categories (NEWS, EKONOMI, etc.). |
| `content` | RichTextField | The news body (using Summernote/CKEditor). |
| `author` | CharField | Author name (default: "Redaksi Suaranusa"). |
| `publish_date` | DateTimeField | Custom publish date for manual ordering. |
| `is_published` | BooleanField | Draft/Published toggle. |
| `is_manual` | BooleanField | Hardcoded `True` to distinguish in templates. |

---

## 🎨 3. Rich Text Editor Strategy

### **Selected: `django-summernote`**
- **Reason:** Most practical for image/video support.
- **Image Support:** Native drag-and-drop upload; saves directly to Django's media storage.
- **Video Support:** Excellent YouTube/Vimeo/Embed support out of the box.
- **Consistency:** Responsive and lightweight compared to full CKEditor builds.

---

## 🔄 4. The Merging Logic (`portal/views/home.py`)

To prevent bugs and ensure high performance, the merging logic will follow these steps:

1. **Concurrent Fetching (Future-proof):**
   - Fetch $N$ articles from Scraper API.
   - Fetch $M$ articles from `ManualArticle` (Local DB).
2. **Normalizing (Crucial Step):**
   - Manual articles are converted to dictionaries using a `to_dict()` method or similar processing to match the Scraper's JSON structure.
3. **Merging & Sorting:**
   - Combine both lists: `combined_list = scraper_list + manual_list`.
   - Sort the combined list by `date` (publish_date) in **Descending** order.
4. **Final Pagination:**
   - Slice the sorted list based on the requested page size (e.g., 12 items).

---

## 📂 5. Media & Static Management
- **Media Setup:** Configure `MEDIA_URL = '/media/'` and `MEDIA_ROOT` in `settings.py`.
- **URL Routing:** Update `core/urls.py` to serve media files during development.
- **Storage:** Images uploaded via Summernote will be stored in `media/django-summernote/`.

---

## 🛡️ 6. Risk Mitigation (Avoiding Bugs)

| Risk | Mitigation Strategy |
|------|---------------------|
| **Missing Field Errors** | Ensure `ManualArticle` provides all keys expected by `home.html` (e.g., `is_video`, `is_gallery`, `source_display`). |
| **Pagination Issues** | Fetch a slightly larger buffer from both sources (e.g., 50 items each) before sorting and slicing to ensure a smooth chronological feed. |
| **Media 404s** | Explicitly check if `main_image` exists before rendering `<img>` tags. |
| **Broken Slugs** | Use Django's `pre_save` signal or override `save()` to auto-generate unique slugs for manual articles. |
| **Dependency Conflict** | Verify `Pillow` and `django-summernote` are added to `requirements.txt`. |

---

## 🚀 7. Implementation Roadmap (Phase 2)

1. **Step 1:** Add `django-summernote` and `Pillow` to `requirements.txt` and install.
2. **Step 2:** Define `ManualArticle` in `portal/models.py` and run migrations.
3. **Step 3:** Configure Media settings in `settings.py` and `urls.py`.
4. **Step 4:** Register `ManualArticle` in `admin.py` with Summernote widget.
5. **Step 5:** Refactor `HomePageView` in `portal/views/home.py` to include merging logic.
6. **Step 6:** Update `portal/views/article_detail.py` to handle both API and Local IDs.
7. **Step 7:** Full end-to-end testing (Create manual news -> Verify on Home -> Verify Detail).

---

**Objective Assessment:** This plan is robust, respects existing architecture, and leverages Django's strengths for content management while keeping the scraper as the primary data engine.
