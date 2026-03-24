# 🔧 Refactoring Plan: Fully Dynamic Scraper

**Date:** 2026-03-23  
**Objective:** Remove hardcoded values, use dynamic discovery & detection  
**Approach:** Step-by-step with testing each progress  

---

## 🎯 CURRENT STATE (HARDCODED)

### comprehensive_scraper.py:
```python
# ❌ HARDCODED
ALL_SUBDOMAINS = [
    'www.detik.com', 'news.detik.com', ...  # 15 domains hardcoded
]

API_ENDPOINTS = {
    'recg_wp': 'https://recg.detik.com/...',  # 7 endpoints hardcoded
    ...
}

TERPOPULER_URLS = [...]  # 5 URLs hardcoded
```

### src/api/main.py:
```python
# Uses comprehensive_scraper which is hardcoded
```

---

## 🎯 TARGET STATE (FULLY DYNAMIC)

### comprehensive_scraper.py:
```python
# ✅ FULLY DYNAMIC
async def scrape_all_subdomains(self):
    # 1. Auto-discover domains
    discovery = DomainDiscovery()
    domains = await discovery.discover()  # ← 30 domains dynamically
    
    # 2. Auto-detect endpoints per domain
    detector = EndpointDetector()
    for domain in domains:
        endpoints = await detector.detect(domain)  # ← 18 endpoints dynamically
        # Use detected endpoints
```

---

## 📋 REFACTORING STEPS

### Step 1: Refactor Domain Discovery Integration
**File:** `src/core/comprehensive_scraper.py`  
**Changes:**
1. Remove `ALL_SUBDOMAINS` hardcoded list
2. Add `DomainDiscovery` import
3. Add `async _discover_domains()` method
4. Update `scrape_all_subdomains()` to use discovery

**Test:**
- Test discovery returns 30 domains
- Test scraping works with discovered domains

**Expected Result:** Get 30 domains dynamically

---

### Step 2: Refactor Endpoint Detection Integration
**File:** `src/core/comprehensive_scraper.py`  
**Changes:**
1. Remove `API_ENDPOINTS` hardcoded dict
2. Add `EndpointDetector` import
3. Add `async _detect_endpoints()` method
4. Update `_scrape_api_endpoints()` to use detected endpoints

**Test:**
- Test endpoint detection per domain
- Test scraping works with detected endpoints

**Expected Result:** Get 7-18 endpoints per domain dynamically

---

### Step 3: Keep Terpopuler (Optional)
**File:** `src/core/comprehensive_scraper.py`  
**Decision:** Keep `TERPOPULER_URLS` hardcoded OR detect from sitemap

**Reason:** 
- Terpopuler is specific URL pattern
- Not discoverable without prior knowledge
- OK to keep as constant

**Test:** Verify terpopuler still works

---

### Step 4: Update REST API Integration
**File:** `src/api/main.py`  
**Changes:**
1. Update `/api/scrape` to use dynamic scraper
2. Ensure all endpoints still work
3. Update error handling

**Test:**
- Test all API endpoints
- Verify backward compatibility

---

### Step 5: Final Integration Test
**Test all together:**
1. Domain discovery working
2. Endpoint detection working
3. Comprehensive scraper working
4. REST API working
5. All tests passing

---

## 📊 IMPLEMENTATION CHECKLIST

### Pre-Implementation:
- [x] Analyze current code
- [x] Test discovery coverage (30 domains - 84.4%)
- [x] Test detection coverage (18 endpoints - 100%)
- [ ] Create refactoring plan
- [ ] Review plan

### Implementation - Step 1 (Domain Discovery):
- [ ] Import DomainDiscovery
- [ ] Remove ALL_SUBDOMAINS constant
- [ ] Add _discover_domains() method
- [ ] Update scrape_all_subdomains() to use discovery
- [ ] Test: Run test_step1_discovery.py
- [ ] Verify: 30 domains discovered

### Implementation - Step 2 (Endpoint Detection):
- [ ] Import EndpointDetector
- [ ] Remove API_ENDPOINTS constant
- [ ] Add _detect_endpoints() method
- [ ] Update _scrape_api_endpoints() to use detection
- [ ] Test: Run test_step2_endpoints.py
- [ ] Verify: 7+ endpoints detected per domain

### Implementation - Step 3 (Terpopuler):
- [ ] Review TERPOPULER_URLS
- [ ] Decision: Keep or make dynamic
- [ ] Test: Run test_terpopuler.py
- [ ] Verify: Terpopuler still works

### Implementation - Step 4 (REST API Update):
- [ ] Update API endpoints
- [ ] Test backward compatibility
- [ ] Test: Run test_step7.py (REST API test)
- [ ] Verify: All API endpoints work

### Implementation - Step 5 (Integration):
- [ ] Run full integration test
- [ ] Run comprehensive test
- [ ] Verify all previous tests still pass
- [ ] Update documentation

---

## 🧪 TEST STRATEGY

### Small Tests (After Each Step):
```bash
# Step 1
python3 test_step1_domain_discovery.py

# Step 2  
python3 test_step2_endpoint_detection.py

# Step 3
python3 test_comprehensive_dynamic.py

# Step 4
python3 test_step7.py  # REST API

# Step 5
python3 test_integration.py
```

### Expected Results:
| Step | Test | Expected Domains | Expected Endpoints |
|------|------|------------------|-------------------|
| 1 | Discovery | 30 | - |
| 2 | Detection | - | 7-18 per domain |
| 3 | Comprehensive | 30 | 7-18 per domain |
| 4 | API | Same as step 3 | Same as step 3 |
| 5 | Integration | 30 | 18 |

---

## 📝 CODE CHANGES PREVIEW

### Before (Hardcoded):
```python
class ComprehensiveScraper:
    ALL_SUBDOMAINS = [
        'www.detik.com',
        'news.detik.com',
        # ... 13 more hardcoded
    ]
    
    API_ENDPOINTS = {
        'recg_wp': 'https://recg.detik.com/...',
        # ... 6 more hardcoded
    }
```

### After (Dynamic):
```python
class ComprehensiveScraper:
    def __init__(self, ...):
        self.discovery = DomainDiscovery()
        self.detector = EndpointDetector()
        # No hardcoded lists!
    
    async def _discover_domains(self):
        return await self.discovery.discover()  # 30 domains
    
    async def _detect_endpoints(self, domain):
        return await self.detector.detect(domain)  # 7-18 endpoints
```

---

## ✅ SUCCESS CRITERIA

### After Refactoring:
- [ ] Zero hardcoded domain lists
- [ ] Zero hardcoded endpoint lists
- [ ] Discovery returns 30+ domains
- [ ] Detection returns 7-18 endpoints per domain
- [ ] All tests passing
- [ ] REST API working
- [ ] Can scrape 500+ articles
- [ ] Documentation updated

---

## 🚀 READY TO IMPLEMENT

**Next Action:** Implement Step 1 - Domain Discovery Integration

**Estimated Time:**
- Step 1: 3 minutes
- Step 2: 3 minutes  
- Step 3: 1 minute
- Step 4: 2 minutes
- Step 5: 2 minutes
- **Total: ~11 minutes**

---

**Proceed with implementation?** ✅
