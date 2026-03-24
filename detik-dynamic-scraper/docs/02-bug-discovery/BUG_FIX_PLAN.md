# 🔧 Bug Fix & Enhancement Plan

**Date:** 2026-03-23  
**Status:** Planning Phase  
**Priority:** HIGH  

---

## 🐛 BUGS TO FIX

### Bug #1: Missing Protocol Handler
**Severity:** 🔴 HIGH  
**Location:** `src/core/content_scraper.py`  
**Current Behavior:**
```python
# Fails when URL lacks protocol
await scraper.scrape('20.detik.com')  # ❌ Error
await scraper.scrape('news.detik.com')  # ❌ Error
```

**Expected Behavior:**
```python
# Should auto-add protocol
await scraper.scrape('20.detik.com')  # ✅ Auto-converts to https://20.detik.com
```

**Fix Strategy:**
1. Add URL validation function at start of `scrape()` method
2. Auto-prepend `https://` if missing
3. Handle edge cases (already has protocol, has `//` prefix, etc.)

**Code Location:**
- File: `src/core/content_scraper.py`
- Method: `scrape()` line ~67
- Add before: `async with httpx.AsyncClient...`

**Implementation:**
```python
def _ensure_protocol(self, url: str) -> str:
    """Ensure URL has protocol."""
    if url.startswith('http://') or url.startswith('https://'):
        return url
    elif url.startswith('//'):
        return 'https:' + url
    else:
        return 'https://' + url
```

---

### Bug #2: NoneType Content-Type Error
**Severity:** 🔴 HIGH  
**Location:** `src/core/content_scraper.py` line ~90  
**Current Behavior:**
```python
content_type = response.headers.get('content-type', '').lower()
# Sometimes headers.get returns None instead of empty string
# Then None.lower() crashes
```

**Root Cause:**
- Bug in previous fix attempt (line 90-104)
- Logic tries to handle None but still calls `.lower()` on None

**Fix Strategy:**
1. Check if content_type is None BEFORE calling .lower()
2. Provide proper fallback
3. Use safer chaining

**Implementation:**
```python
# Current (BUGGY):
content_type = response.headers.get('content-type', '')
if content_type:
    content_type = content_type.lower()  # Still fails if None
    
# Fixed:
content_type = response.headers.get('content-type') or ''
content_type = content_type.lower()  # Now safe
```

---

## 📊 ENHANCEMENTS NEEDED

### Enhancement #1: Complete Subdomain Coverage
**Priority:** 🟡 MEDIUM  
**Current:** 12/32 subdomains (37.5%)  
**Target:** 32/32 subdomains (100%)  

**Missing Subdomains:**
```python
# Add to parameter_extractor.py domain_map
'edu.detik.com': 'acc-detikedu',
'event.detik.com': 'acc-detikevent',
'foto.detik.com': 'acc-detikfoto',
'karir.detik.com': 'acc-detikkarir',
'kemiri.detik.com': 'acc-detikkemiri',
'pasangmata.detik.com': 'acc-detikpasangmata',
'fyb.detik.com': 'acc-detikfyb',
'vod.detik.com': 'acc-detikvod',
'explore-api.detik.com': 'acc-detikexplore',
# ... 11 more
```

**Implementation Location:**
- File: `src/core/parameter_extractor.py`
- Method: `_extract_acctype()` line ~111
- Expand: `domain_map` dictionary

---

### Enhancement #2: Homepage Scraping
**Priority:** 🟡 MEDIUM  
**Current:** Only API endpoint scraping  
**Target:** Add HTML homepage scraping  

**Strategy:**
Each channel homepage contains 15-59 articles that may not be in API.

**Implementation:**
```python
# In content_scraper.py
async def scrape_homepage(self, channel: str) -> List[Dict]:
    """Scrape articles from channel homepage."""
    url = f"https://{channel}.detik.com"
    articles = await self.scrape(url, response_type='html')
    return articles
```

**Channels to Scrape:**
- news, finance, sport, hot, inet, travel, food, health, oto, wolipop
- edu, 20, event, foto, karir, etc.

---

### Enhancement #3: Terpopuler Integration
**Priority:** 🟢 LOW  
**Current:** Not implemented  
**Target:** Scrape trending articles  

**Endpoints:**
```python
TERPOPULER_URLS = [
    'https://www.detik.com/terpopuler',      # All time
    'https://www.detik.com/terpopuler/1',    # 1 day
    'https://www.detik.com/terpopuler/3',    # 3 days
    'https://www.detik.com/terpopuler/7',    # 7 days
    'https://www.detik.com/terpopuler/30',   # 30 days
]
```

**Implementation:**
Add to `content_scraper.py` as specialized method.

---

## 🎯 IMPLEMENTATION PRIORITY

### Phase 1: Critical Bug Fixes (HIGH - Do Now)
1. ✅ Fix Bug #1: Protocol handler
2. ✅ Fix Bug #2: Content-type None error
3. ✅ Test both fixes
4. ✅ Verify all existing tests still pass

**Estimated Time:** 5 minutes  
**Impact:** Fixes crashes, enables domain scraping  

---

### Phase 2: Complete Coverage (MEDIUM - After Bug Fixes)
5. ⏳ Add all 32 subdomain acctypes
6. ⏳ Implement homepage scraping
7. ⏳ Test scraping from all channels
8. ⏳ Update integration test

**Estimated Time:** 10 minutes  
**Impact:** 100% subdomain coverage, more articles  

---

### Phase 3: Advanced Features (LOW - Optional)
9. ⏳ Add Terpopuler scraping
10. ⏳ Optimize parallel scraping
11. ⏳ Add video-specific handlers
12. ⏳ Implement full 50+ subdomain support

**Estimated Time:** 15 minutes  
**Impact:** Complete feature parity with research  

---

## 📋 FIX CHECKLIST

### Pre-Fix:
- [x] All bugs identified
- [x] Documentation reviewed
- [x] Test cases created
- [x] Fix strategy planned

### During Fix:
- [ ] Fix Bug #1 (protocol)
- [ ] Fix Bug #2 (content-type)
- [ ] Add test for protocol handling
- [ ] Add test for None content-type
- [ ] Run all existing tests

### Post-Fix:
- [ ] Verify no regressions
- [ ] Update test results
- [ ] Document changes
- [ ] Update PROGRESS.md

---

## 🧪 TEST PLAN

### Bug Fix Tests:

**Test 1: Protocol Auto-Add**
```python
# Should work after fix
await scraper.scrape('20.detik.com')
await scraper.scrape('news.detik.com')
await scraper.scrape('//cdn.detik.com/file.jpg')
```

**Test 2: None Content-Type**
```python
# Should handle gracefully
# Mock response with None content-type
# Should not crash, should detect from content
```

**Test 3: Integration**
```python
# Full workflow with domain-only URLs
domains = ['news.detik.com', 'finance.detik.com', 'sport.detik.com']
for domain in domains:
    articles = await scraper.scrape(domain)
    assert len(articles) > 0
```

---

## 📊 SUCCESS CRITERIA

### Bug Fixes:
- ✅ No crashes on domain-only URLs
- ✅ No crashes on None content-type
- ✅ All existing tests still pass
- ✅ New test cases added and passing

### Enhancement:
- ✅ 32/32 subdomains mapped
- ✅ Homepage scraping works
- ✅ Can scrape 1000+ articles total
- ✅ Integration test covers all channels

---

## 🚀 EXECUTION ORDER

1. **NOW:** Fix Bug #1 (protocol)
2. **NOW:** Fix Bug #2 (content-type)
3. **NOW:** Test fixes
4. **NEXT:** Add missing subdomains
5. **NEXT:** Implement homepage scraping
6. **LATER:** Advanced features

---

**Ready to implement fixes!** 🔧
