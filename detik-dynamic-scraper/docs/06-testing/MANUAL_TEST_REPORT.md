# 🧪 Manual Test Report - Bug Identification

**Date:** 2026-03-23  
**Tester:** Manual Testing Phase  
**Objective:** Test all endpoints, identify bugs, read documentation  

---

## 🐛 BUGS IDENTIFIED

### Bug #1: Missing Protocol in URL
**Severity:** HIGH  
**Location:** `src/core/content_scraper.py`  
**Error Message:**
```
⚠️ Request URL is missing an 'http://' or 'https://' protocol.
❌ Failed to scrape 20.detik.com
```

**Root Cause:**
- When scraping, sometimes domain is passed without protocol
- `20.detik.com` should be `https://20.detik.com`

**Impact:**
- Cannot scrape domains without explicit protocol
- Fails for all subdomain scraping

---

### Bug #2: NoneType Attribute Error
**Severity:** HIGH  
**Location:** `src/core/content_scraper.py` line ~90
**Error Message:**
```
⚠️ 'NoneType' object has no attribute 'lower'
❌ Failed to scrape https://20.detik.com
```

**Root Cause:**
- In `content_scraper.py`, checking `content_type.lower()` when `content_type` is None
- Happens when `response.headers.get('content-type')` returns None

**Impact:**
- Scraper crashes when content-type header is missing
- Cannot handle responses without content-type

---

## 📊 DOCUMENTATION REVIEW

### Key Findings from Existing Research:

#### 1. **32 Subdomains Discovered** (from detik_comprehensive_summary.txt)
```
Main Content Channels (10):
- news, finance, sport, hot, inet, travel, food, health, oto, wolipop

API Endpoints (4):
- recg, rech, rech20, explore-api

Special Services (18):
- 20 (video), connect (auth), apicomment, cdnstatic, cdnv, etc.
```

#### 2. **7 API Endpoints Documented** (Highly tested!)
```
recg.detik.com/article-recommendation/wp/{user_id}
recg.detik.com/article-recommendation/detail/{user_id}
recg.detik.com/article-recommendation/index/{user_id}
recg.detik.com/article-recommendation/sticky/{user_id}
rech.detik.com/article-recommendation/wp/{user_id}
rech.detik.com/article-recommendation/detail/{user_id}
rech20.detik.com/article-recommendation/detail/{user_id}
```

#### 3. **Account Types per Channel** (from DETIK_COMPLETE_FLOW_DOCUMENTATION.md)
```
acc-detikcom      → www.detik.com
acc-detiknews     → news.detik.com
acc-detikfinance  → finance.detik.com
acc-detiksport    → sport.detik.com
acc-detikhot      → hot.detik.com
acc-detikinet     → inet.detik.com
acc-detiktravel   → travel.detik.com
acc-detikfood     → food.detik.com
acc-detikhealth   → health.detik.com
acc-detikoto      → oto.detik.com
acc-detikwolipop  → wolipop.detik.com
acc-detik20       → 20.detik.com
```

#### 4. **Successful Scraping Record** (from summary)
- 840 articles successfully scraped
- 53 unique IDs
- 30 articles per channel average
- All 10 channels tested and working

---

## 🎯 MISSING IMPLEMENTATIONS

### 1. **Not All 32 Subdomains Covered**
Current implementation only covers 12 domains (acctype mapping).
Missing:
- edu.detik.com (education)
- event.detik.com (events)
- foto.detik.com (photos)
- karir.detik.com (career)
- And 18 other subdomains

### 2. **Channel Homepage Scraping Not Implemented**
From documentation: Each channel homepage has 15-59 articles.
Current scraper only uses API endpoints, not homepage scraping.

### 3. **Terpopuler Pages Not Integrated**
Documentation shows:
- /terpopuler (all time)
- /terpopuler/1 (1 day)
- /terpopuler/3 (3 days)
- /terpopuler/7 (7 days)
- /terpopuler/30 (30 days)

Not yet integrated in dynamic scraper.

### 4. **Video Content (20.detik.com) Not Working**
Bug prevents video content scraping from 20.detik.com

---

## 📋 TEST RESULTS BY ENDPOINT

### ✅ Working Endpoints:
- `/health` - OK
- `/api/discover-domains` - OK (finds 30 domains)
- `/api/detect-endpoints` - OK (finds 18-20 endpoints)
- `/api/statistics` - OK

### ⚠️ Partially Working:
- `/api/scrape` - Works for API URLs, fails for domain-only URLs
- `/api/articles/search` - Works but empty DB initially

### ❌ Issues Found:
- Scraping without protocol (20.detik.com vs https://20.detik.com)
- Content-type None error
- Cannot scrape HTML homepages yet

---

## 📖 INSIGHTS FROM DOCUMENTATION

### From DETIK_API_FLOW_DOCUMENTATION.md:
1. **User ID Pattern:** `{cookie1}.{cookie2}.{timestamp}`
2. **Size Parameter:** Can request 1-100+ articles
3. **IDs Parameter:** Can be "undefined" or specific article IDs
4. **Nocache:** Always set to 1 for fresh data

### From DETIK_COMPLETE_FLOW_DOCUMENTATION.md:
1. **50+ Subdomains exist** in Detik ecosystem
2. **Each channel has different content structure**
3. **Parallel scraping is recommended** for speed
4. **Rate limiting is important** (1-2 second delays)

### From detik_comprehensive_scraper.py (existing):
1. **Successfully scraped 840 articles** using 7 API endpoints
2. **30 articles per channel** is optimal
3. **User ID can be test/random** for public endpoints
4. **All channels tested and verified working**

---

## 🎯 NEXT STEPS (Priority Order)

### High Priority:
1. **Fix Bug #1:** Add protocol validation/auto-prepend
2. **Fix Bug #2:** Handle None content-type safely
3. **Test all API endpoints** with proper URLs

### Medium Priority:
4. **Add missing acctypes** for all 32 subdomains
5. **Implement homepage scraping** for each channel
6. **Add Terpopuler page scraping**

### Low Priority:
7. **Optimize parallel scraping** for 32 subdomains
8. **Add video-specific handling** for 20.detik.com
9. **Implement full coverage** for all 50+ subdomains

---

## 📊 COVERAGE ANALYSIS

**Current Coverage:**
- Domains: 12/32 (37.5%)
- API Endpoints: 7/7 (100% of known)
- Channels: 10/10 (100% main channels)
- Features: 5/8 (62.5%)

**Target Coverage:**
- Domains: 32/32 (100%)
- API Endpoints: 7/7 (100%)
- Channels: 12/12 (100% including edu, 20)
- Features: 8/8 (100%)

---

## 🔧 READY FOR BUG FIX PLANNING

All bugs identified and documented.
Ready to create fix planning document.
