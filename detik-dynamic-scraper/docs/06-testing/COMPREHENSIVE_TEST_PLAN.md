# 📋 Comprehensive Test Plan - All 30 Domains

**Date:** 2026-03-23  
**Objective:** Test scraping with ALL 30 discovered domains  
**Approach:** Batch testing with incremental verification  

---

## 🎯 OBJECTIVE

Test comprehensive scraper dengan semua 30 domains yang di-discover dinamis untuk membuktikan sistem fully dynamic bekerja sempurna.

---

## 📊 CURRENT STATE

From discovery test:
- **Total domains discovered:** 30
- **Content channels:** 20 (filtered)
- **Previous test:** Only 3 domains tested

**Target:** Test ALL 20 content channels

---

## 🚨 RISK ASSESSMENT

### Potential Issues:
1. ⚠️ Some domains might timeout
2. ⚠️ Some domains might have no content
3. ⚠️ Rate limiting from too many requests
4. ⚠️ Memory usage with large dataset

### Mitigation Strategy:
- ✅ Batch testing (5 domains per batch)
- ✅ Rate limiting (0.5s delay)
- ✅ Max workers: 3 (parallel control)
- ✅ Target: 10 articles per domain (reasonable)
- ✅ Test incrementally

---

## 📋 TEST STRATEGY

### Phase 1: Small Batch Test (5 domains)
**Purpose:** Verify batch scraping works
**Domains:** First 5 content channels
**Target:** 10 articles per domain
**Expected:** ~50 articles total

### Phase 2: Medium Batch Test (10 domains)
**Purpose:** Test scalability
**Domains:** First 10 content channels
**Target:** 10 articles per domain
**Expected:** ~100 articles total

### Phase 3: Large Batch Test (15 domains)
**Purpose:** Test larger scale
**Domains:** First 15 content channels
**Target:** 10 articles per domain
**Expected:** ~150 articles total

### Phase 4: Full Test (20 domains)
**Purpose:** Full comprehensive test
**Domains:** ALL 20 content channels
**Target:** 15 articles per domain
**Expected:** ~300 articles total

---

## 📝 IMPLEMENTATION PLAN

### Step 1: Create Batch Test Script
**File:** `test_batch_scraping.py`
**Features:**
- Accept batch size parameter
- Display progress per domain
- Show statistics after each batch
- Handle errors gracefully

### Step 2: Test Small Batch (5 domains)
**Command:** `python3 test_batch_scraping.py --batch=5`
**Validation:**
- At least 40 articles scraped
- No crashes
- All domains processed

### Step 3: Test Medium Batch (10 domains)
**Command:** `python3 test_batch_scraping.py --batch=10`
**Validation:**
- At least 80 articles scraped
- Performance acceptable
- Memory usage OK

### Step 4: Test Large Batch (15 domains)
**Command:** `python3 test_batch_scraping.py --batch=15`
**Validation:**
- At least 120 articles scraped
- System stable
- Quality maintained

### Step 5: Full Comprehensive Test (20 domains)
**Command:** `python3 test_comprehensive_full.py`
**Validation:**
- At least 200 articles scraped
- All domains attempted
- Results stored in database
- Export successful

---

## ✅ SUCCESS CRITERIA

### Per Batch:
- [ ] No system crashes
- [ ] At least 80% domains return articles
- [ ] Average quality score > 0.4
- [ ] Memory usage acceptable
- [ ] Processing time reasonable

### Overall:
- [ ] All 20 content channels tested
- [ ] At least 200 articles total
- [ ] Database storage successful
- [ ] Export to JSON successful
- [ ] Performance metrics acceptable

---

## 📊 EXPECTED RESULTS

### Domains to Test (20 content channels):
```
1. 20.detik.com
2. event.detik.com
3. finance.detik.com
4. food.detik.com
5. foto.detik.com
6. fyb.detik.com
7. health.detik.com
8. hot.detik.com
9. inet.detik.com
10. karir.detik.com
11. newpolong.detik.com
12. news.detik.com
13. oto.detik.com
14. pasangmata.detik.com
15. rech20.detik.com
16. sport.detik.com
17. temanmudik.detik.com
18. travel.detik.com
19. wolipop.detik.com
20. www.detik.com
```

### Performance Targets:
| Metric | Target | Acceptable |
|--------|--------|------------|
| Domains attempted | 20 | 20 |
| Domains successful | 18+ | 16+ |
| Total articles | 300+ | 200+ |
| Avg quality | 0.5+ | 0.4+ |
| Time per domain | <30s | <60s |
| Total time | <10min | <15min |

---

## 🧪 TEST EXECUTION SEQUENCE

1. ✅ Create test script
2. ⏳ Run batch test (5 domains)
3. ⏳ Validate results
4. ⏳ Run batch test (10 domains)
5. ⏳ Validate results
6. ⏳ Run full test (20 domains)
7. ⏳ Analyze final results
8. ⏳ Create final report

---

## 📋 VALIDATION CHECKLIST

### After Each Batch:
- [ ] Check logs for errors
- [ ] Verify article count
- [ ] Check quality scores
- [ ] Review memory usage
- [ ] Confirm no crashes

### After Full Test:
- [ ] All domains attempted
- [ ] Database populated
- [ ] Export successful
- [ ] Statistics generated
- [ ] Performance acceptable

---

## 🎯 DELIVERABLES

1. `test_batch_scraping.py` - Batch test script
2. `test_comprehensive_full.py` - Full test script
3. `COMPREHENSIVE_TEST_RESULTS.md` - Results report
4. Database with 200+ articles
5. JSON export with all data

---

**Estimated Time:** 15-20 minutes total  
**Risk Level:** LOW (incremental testing)  
**Ready to implement:** ✅

