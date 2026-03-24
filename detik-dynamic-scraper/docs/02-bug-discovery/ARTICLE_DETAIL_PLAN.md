# 📄 Article Detail Scraping & Display Plan

**Date:** 2026-03-24  
**Objective:** Scrape full article content & create display page  
**Approach:** Step-by-step with testing  

---

## 📊 CURRENT STATE ANALYSIS

### What We Have Now:
```
✅ Article metadata:
   - Title, description, URL
   - Image, tags, category
   - Publish date, source
   - Quality score

❌ Missing:
   - Full article content (body text)
   - Author details
   - Related articles
   - Comments
```

### Why Missing?
Current scraper gets data from:
1. **API endpoints** → Only metadata
2. **Homepage HTML** → Only article list

To get full content:
→ Need to scrape **individual article detail pages**

---

## 🎯 COMPLETE FLOW EXPLANATION

### Current Flow (Metadata Only):
```
1. Discover domains (30 domains)
   ↓
2. Detect endpoints (18 endpoints)
   ↓
3. Scrape from API/homepage
   ↓
4. Get metadata (title, URL, description)
   ↓
5. Store in database
   ↓
6. Display in dashboard
```

### NEW Flow (With Full Content):
```
1. Discover domains (30 domains)
   ↓
2. Detect endpoints (18 endpoints)
   ↓
3. Scrape from API/homepage (metadata)
   ↓
4. Get article URLs
   ↓
5. **Scrape detail page for each URL** ← NEW!
   ↓
6. Extract full content (body text)
   ↓
7. Store complete data
   ↓
8. Display with full content
```

---

## 📋 IMPLEMENTATION PLAN

### Step 1: Create Article Detail Scraper
**File:** `src/core/article_detail_scraper.py`  
**Tasks:**
- Scrape article detail page
- Extract full content (body text)
- Extract author, related articles
- Handle different article formats

**Test:**
- Test with 1 article URL
- Verify content extracted

**Expected:** Full article content retrieved

---

### Step 2: Integrate with Comprehensive Scraper
**File:** Update `src/core/comprehensive_scraper.py`  
**Tasks:**
- Add option to scrape detail
- Scrape details after getting URLs
- Store full content

**Test:**
- Scrape 5 articles with details
- Verify database has content

**Expected:** Full content in database

---

### Step 3: Update Database Schema
**File:** `src/storage/database.py`  
**Tasks:**
- Ensure `content` field stores large text
- Add fields for author_details, related_articles

**Test:**
- Insert article with full content
- Retrieve and verify

**Expected:** Database stores full content

---

### Step 4: Create Simple Display Page
**File:** `simple_article_page.html`  
**Tasks:**
- HTML page to display all articles
- Consume REST API
- Show title, image, description, content
- Simple styling

**Test:**
- Open in browser
- See articles displayed
- Click to read full content

**Expected:** Clean article display

---

### Step 5: Add API Endpoint for Article Details
**File:** Update `src/api/main.py`  
**Tasks:**
- Add endpoint to get article with full content
- Add endpoint to scrape article detail on demand

**Test:**
- Call API endpoint
- Get full article content

**Expected:** API returns full content

---

## 🔄 COMPLETE API FLOW

### Flow 1: Scrape Metadata + Content
```
POST /api/scrape
{
  "url": "https://news.detik.com",
  "scrape_details": true  ← Enable detail scraping
}

Response:
{
  "articles": [
    {
      "title": "...",
      "url": "...",
      "description": "...",
      "content": "Full article text here..."  ← NEW!
    }
  ]
}
```

### Flow 2: Get Article with Content
```
GET /api/articles/{article_id}?include_content=true

Response:
{
  "id": "8412424",
  "title": "...",
  "content": "Full article text...",
  "author": "...",
  "related_articles": [...]
}
```

### Flow 3: Scrape Article Detail On-Demand
```
POST /api/articles/{article_id}/scrape-detail

Response:
{
  "success": true,
  "content_length": 5000,
  "content": "..."
}
```

---

## 📝 SIMPLE DISPLAY PAGE STRUCTURE

### HTML Structure:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Detik Articles</title>
    <style>
        /* Simple, clean styling */
    </style>
</head>
<body>
    <header>
        <h1>📰 Detik Articles</h1>
    </header>
    
    <div id="articles">
        <!-- Articles loaded via JavaScript -->
    </div>
    
    <script>
        // Fetch from API
        fetch('http://localhost:8000/api/articles/search')
            .then(r => r.json())
            .then(data => displayArticles(data.articles));
    </script>
</body>
</html>
```

### Features:
- ✅ Fetch articles from REST API
- ✅ Display title, image, description
- ✅ Show full content (if available)
- ✅ Link to original article
- ✅ Simple, clean design
- ✅ Responsive layout

---

## 🧪 TESTING STRATEGY

### Step 1 Test:
```bash
python3 test_article_detail_scraper.py
# Test: Scrape 1 article detail
# Expected: Full content extracted
```

### Step 2 Test:
```bash
python3 test_comprehensive_with_details.py
# Test: Scrape 5 articles with details
# Expected: All have full content
```

### Step 3 Test:
```bash
python3 test_database_content.py
# Test: Store and retrieve full content
# Expected: Content persisted correctly
```

### Step 4 Test:
```bash
# Open simple_article_page.html in browser
# Expected: Articles displayed from API
```

### Step 5 Test:
```bash
curl http://localhost:8000/api/articles/8412424
# Expected: JSON with full content
```

---

## 📊 DELIVERABLES

1. **article_detail_scraper.py** - Detail scraper
2. **Updated comprehensive_scraper.py** - Integration
3. **Updated database.py** - Content storage
4. **simple_article_page.html** - Display page
5. **Updated main.py** - New API endpoints
6. **API_USAGE_GUIDE.md** - Complete API documentation
7. **Test files** - Verification scripts

---

## ⏱️ TIME ESTIMATE

- Step 1: Article detail scraper - 5 minutes
- Step 2: Integration - 3 minutes
- Step 3: Database update - 2 minutes
- Step 4: Simple page - 5 minutes
- Step 5: API endpoints - 3 minutes
- Testing - 5 minutes
- **Total: ~23 minutes**

---

## ✅ SUCCESS CRITERIA

### After Implementation:
- [ ] Can scrape full article content
- [ ] Database stores full content
- [ ] API returns full content
- [ ] Simple page displays articles
- [ ] All tests passing

---

**Ready to implement Step 1: Article Detail Scraper** ✅
