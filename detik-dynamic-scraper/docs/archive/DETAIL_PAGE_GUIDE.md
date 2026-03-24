# 📄 Article Detail Page - Complete Guide

## ✅ WHAT'S IMPLEMENTED

### 1. Article Detail Page
**File:** `article_detail.html`

**Features:**
- ✅ Full article display
- ✅ Title, image, metadata
- ✅ Description and full content
- ✅ Tags and quality score
- ✅ On-demand content scraping
- ✅ Link to original article

---

### 2. API Endpoints

#### GET /detail
Serves article detail HTML page

**Example:**
```
http://localhost:8000/detail?id=8412424
```

#### GET /api/articles/{id}
Get article data by ID

**Example:**
```
curl http://localhost:8000/api/articles/8412424
```

#### POST /api/articles/{id}/scrape-detail
Scrape full content for article on-demand

**Example:**
```bash
curl -X POST http://localhost:8000/api/articles/8412424/scrape-detail
```

---

## 🔄 COMPLETE USER FLOW

### Flow 1: View Article with Existing Metadata

```
1. User opens: http://localhost:8000/
2. Sees 538 articles in grid
3. Clicks on article card
4. Redirects to: http://localhost:8000/detail?id=8412424
5. Shows article detail page
6. Displays: title, description, metadata
7. If full content available: Shows content
8. If no content: Shows "Scrape Full Content" button
```

### Flow 2: Scrape Full Content On-Demand

```
1. User on detail page (no full content yet)
2. Sees: "📄 Full content not available"
3. Clicks: "🔍 Scrape Full Content Now"
4. JavaScript calls: POST /api/articles/{id}/scrape-detail
5. API scrapes article from detik.com
6. Extracts full content (body text)
7. Stores in database
8. Page refreshes automatically
9. Full content now displays!
```

---

## 🎯 HOW TO USE

### Step 1: Start API Server
```bash
cd detik-dynamic-scraper
source ../venv_detik/bin/activate
python3 -m uvicorn src.api.main:app --reload
```

### Step 2: Open Main Page
```
http://localhost:8000/
```

### Step 3: Browse Articles
- See 538 articles in grid
- Use search to filter
- Click any article

### Step 4: View Detail
- Article detail page opens
- Shows metadata and description
- If no full content: Click "Scrape Full Content"
- Wait 5-10 seconds
- Full content appears!

---

## 📊 WHAT DATA IS SHOWN

### On List Page (simple_article_page.html):
- Title
- Description (excerpt)
- Image
- Source
- Quality score
- Tags

### On Detail Page (article_detail.html):
- ✅ Everything from list page
- ✅ Full metadata (author, date, category)
- ✅ Full content (body text) - if scraped
- ✅ Related articles - if available
- ✅ Link to original article

---

## 🔍 ON-DEMAND SCRAPING

**When you click "Scrape Full Content":**

1. Frontend calls API
2. API fetches article URL from database
3. Scrapes article detail page from detik.com
4. Extracts:
   - Full body text
   - Author name
   - Related articles
5. Stores in database
6. Returns success
7. Page refreshes with content

**Time:** ~5-10 seconds per article

---

## 🎨 FEATURES

### Article Detail Page:
- ✅ Clean, readable layout
- ✅ Large hero image
- ✅ Quality score badge
- ✅ Tags display
- ✅ Full metadata
- ✅ Formatted content
- ✅ On-demand scraping
- ✅ Link to original
- ✅ Back to articles link

### URL Structure:
```
Main page:    http://localhost:8000/
Detail page:  http://localhost:8000/detail?id={article_id}
API endpoint: http://localhost:8000/api/articles/{article_id}
Scrape:       http://localhost:8000/api/articles/{article_id}/scrape-detail
```

---

## 🧪 TESTING

### Test 1: View Article with ID
```
http://localhost:8000/detail?id=8412424
```

### Test 2: Get Article Data
```bash
curl http://localhost:8000/api/articles/8412424 | jq
```

### Test 3: Scrape Full Content
```bash
curl -X POST http://localhost:8000/api/articles/8412424/scrape-detail
```

### Test 4: Complete User Flow
1. Open http://localhost:8000/
2. Click any article
3. See detail page
4. Click "Scrape Full Content" if shown
5. Wait for content to load
6. Read full article!

---

## ✅ COMPLETE FLOW DIAGRAM

```
User
 ↓
Opens: http://localhost:8000/
 ↓
Sees: Grid of 538 articles
 ↓
Clicks: Article card
 ↓
Redirects: /detail?id=8412424
 ↓
Loads: article_detail.html
 ↓
JavaScript: fetch('/api/articles/8412424')
 ↓
API: Returns article data
 ↓
Display: Title, image, metadata, description
 ↓
Check: Has full content?
 ├─ YES → Display full content
 └─ NO → Show "Scrape Full Content" button
      ↓
      User clicks button
      ↓
      POST /api/articles/8412424/scrape-detail
      ↓
      API scrapes from detik.com
      ↓
      Stores content in database
      ↓
      Page refreshes
      ↓
      Full content displays! ✅
```

---

## 🎉 BENEFITS

**Before:**
- Click article → Opens detik.com
- Leaves your site
- No tracking
- No full content storage

**Now:**
- Click article → Opens detail page
- Stays on your site
- Full control
- Can scrape content on-demand
- Store in your database
- Better user experience!

---

**Status:** ✅ IMPLEMENTED & READY TO TEST

**Try now:**
```bash
python3 -m uvicorn src.api.main:app --reload
# Open: http://localhost:8000/
# Click any article!
```

