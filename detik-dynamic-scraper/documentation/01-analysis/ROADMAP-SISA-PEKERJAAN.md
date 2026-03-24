# 🗺️ REMAINING ISSUES - ANALYSIS & ROADMAP

**Tanggal:** 24 Maret 2026  
**Status:** 8/26 Critical Bugs Fixed, 18 Remaining Issues  
**Progress:** 31% Complete

---

## 📊 CURRENT STATUS

### **Completed (Sprint 1):**
✅ 8 Critical Bugs Fixed (100% tested)
- PRIMARY KEY NULL
- Duplicate Data
- Memory Leak
- Connection Leak
- N+1 Query
- Bare Exceptions
- URL Validation
- Logging System

### **Remaining Work:**
🔴 **10 HIGH Priority Issues**  
🟡 **8 MEDIUM Priority Issues**

---

## 🎯 REMAINING ISSUES BREAKDOWN

### **Category Distribution:**

```
Database Issues:     9 total (1 fixed, 8 remaining)
  ✅ PRIMARY KEY NULL (fixed)
  ✅ Duplicate Data (fixed)
  ✅ N+1 Query (fixed)
  ✅ Connection Leak (fixed)
  🔴 5 HIGH remaining
  🟡 1 MEDIUM remaining

Performance Issues:  8 total (1 fixed, 7 remaining)
  ✅ N+1 Query (fixed)
  ✅ Memory Leak (fixed)
  🟡 6 MEDIUM remaining

Error Handling:      5 total (2 fixed, 3 remaining)
  ✅ Bare Exceptions (fixed)
  ✅ URL Validation (fixed)
  🔴 3 HIGH remaining

Architecture:        4 total (0 fixed, 4 remaining)
  🔴 2 HIGH remaining
  🟡 2 MEDIUM remaining
```

---

## 🔴 HIGH PRIORITY ISSUES (10 Total)

### **BP #1: 113 Print Statements → Logging** 
**Status:** 🟢 PARTIALLY DONE (50%)  
**Priority:** HIGH  
**Effort:** 2-3 days

**Current State:**
- ✅ Logging module created
- ✅ 3 core modules migrated (database, content_scraper, comprehensive_scraper)
- ❌ Masih ada ~80 print statements di modules lain

**Remaining Work:**
```python
# Files masih perlu di-migrate:
- article_detail_scraper.py (15 prints)
- data_normalizer.py (14 prints)
- domain_discovery.py (10 prints)
- endpoint_detector.py (10 prints)
- parameter_extractor.py (9 prints)
- API main.py (3 prints)
- Dashboard pages (20+ prints)
```

**Implementation Plan:**
1. Add logger import ke setiap file
2. Replace print dengan logger.info/warning/error
3. Test setiap modul
4. Update dashboard untuk logging UI

**Impact:** HIGH - Production debugging dan monitoring
**Complexity:** LOW - Straightforward replacement

---

### **BP #2: Global Database Instance di API**
**Priority:** 🔴 HIGH  
**Effort:** 1 day

**Problem:**
```python
# src/api/main.py line 25
db = Database("data/comprehensive_full_test.db")  # ❌ Global!
normalizer = DataNormalizer()  # ❌ Global!
```

**Issues:**
- Thread safety problems
- Single connection untuk semua requests
- Cannot use different DB for testing
- Connection leak saat restart

**Solution:**
```python
from fastapi import Depends

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/articles/{id}")
async def get_article(id: str, db: Database = Depends(get_db)):
    return db.get_article(id)
```

**Impact:** HIGH - Thread safety, testability
**Complexity:** MEDIUM - Perlu update semua endpoints

---

### **BP #3: Hardcoded Database Path**
**Priority:** 🔴 HIGH  
**Effort:** 0.5 day

**Problem:**
```python
# Inconsistent paths across codebase
db = Database("data/comprehensive_full_test.db")
db = Database("data/scraper.db")
db = Database("data/dashboard_scraping.db")
# 21 different database files!
```

**Solution:**
```python
import os

# Use environment variable
DB_PATH = os.getenv('DATABASE_URL', 'data/scraper.db')
TEST_DB_PATH = os.getenv('TEST_DATABASE_URL', 'data/test_scraper.db')

# Single source of truth
from config import settings
db = Database(settings.DATABASE_URL)
```

**Impact:** HIGH - Consistency, testing
**Complexity:** LOW - Simple refactor

---

### **BP #4: No Input Validation di API**
**Priority:** 🔴 HIGH  
**Effort:** 2 days

**Problem:**
```python
@app.post("/api/scrape")
async def scrape(request: ScrapeRequest):
    # ❌ No validation:
    # - URL format tidak di-check
    # - max_pages bisa 99999
    # - No rate limiting
```

**Solution:**
```python
from pydantic import BaseModel, Field, HttpUrl, validator

class ScrapeRequest(BaseModel):
    url: HttpUrl  # Auto-validates URL
    max_pages: int = Field(default=1, ge=1, le=100)
    
    @validator('url')
    def validate_url(cls, v):
        if not str(v).strip():
            raise ValueError("URL cannot be empty")
        # Add more validations
        return v
```

**Impact:** HIGH - Security, stability
**Complexity:** MEDIUM - Need comprehensive validation

---

### **BP #5: No Error Handling di Async Functions**
**Priority:** 🔴 HIGH  
**Effort:** 1 day

**Problem:**
```python
async def scrape_all_subdomains(self, ...):
    tasks = []
    for subdomain in subdomains:
        # ❌ No try/except
        task = self._scrape_subdomain(subdomain)
        tasks.append(task)
    
    # Jika 1 task crash, semua bisa terganggu
    results = await asyncio.gather(*tasks)
```

**Solution:**
```python
async def safe_scrape_subdomain(subdomain):
    try:
        return await self._scrape_subdomain(subdomain)
    except Exception as e:
        logger.error(f"Error scraping {subdomain}: {e}", exc_info=True)
        return {'subdomain': subdomain, 'error': str(e), 'articles': []}

# Use safe wrapper
tasks = [safe_scrape_subdomain(sd) for sd in subdomains]
results = await asyncio.gather(*tasks)
```

**Impact:** HIGH - Reliability, error tracking
**Complexity:** MEDIUM - Multiple async functions

---

### **BP #6: Cache Tidak Pernah Di-Expire**
**Priority:** 🔴 HIGH  
**Effort:** 0.5 day

**Problem:**
```python
# src/core/comprehensive_scraper.py
self._endpoint_cache = {}  # ❌ Cache forever!

async def _detect_endpoints(self, domain):
    if domain in self._endpoint_cache:
        return self._endpoint_cache[domain]  # Stale data!
```

**Solution:**
```python
from datetime import datetime, timedelta

self._endpoint_cache = {}  # {domain: (endpoints, timestamp)}

async def _detect_endpoints(self, domain):
    if domain in self._endpoint_cache:
        endpoints, timestamp = self._endpoint_cache[domain]
        # Expire setelah 1 jam
        if datetime.now() - timestamp < timedelta(hours=1):
            return endpoints
        else:
            logger.info(f"Cache expired for {domain}, re-detecting")
    
    # Detect and cache
    endpoints = await self._do_detect(domain)
    self._endpoint_cache[domain] = (endpoints, datetime.now())
    return endpoints
```

**Impact:** MEDIUM-HIGH - Data freshness
**Complexity:** LOW - Simple timestamp check

---


### **BP #7: Tight Coupling - Database di Semua Layer**
**Priority:** 🔴 HIGH  
**Effort:** 3 days

**Problem:**
```python
# API layer directly uses Database
db = Database()

# Scraper juga directly save ke DB
db.insert_article(article)

# No abstraction layer!
```

**Issues:**
- Violates Single Responsibility Principle
- Sulit testing (mock database)
- Sulit ganti database (SQLite → PostgreSQL)
- Business logic mixed dengan data access

**Solution: Repository Pattern**
```python
# 1. Repository Layer
class ArticleRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def save(self, article: Dict) -> bool:
        return self.db.insert_article(article)
    
    def find_by_id(self, id: str) -> Optional[Dict]:
        return self.db.get_article(id)
    
    def search(self, filters: Dict) -> List[Dict]:
        return self.db.search_articles(**filters)

# 2. Service Layer
class ScraperService:
    def __init__(self, repo: ArticleRepository):
        self.repo = repo
        self.scraper = ContentScraper()
    
    async def scrape_and_save(self, url: str):
        articles = await self.scraper.scrape(url)
        for article in articles:
            self.repo.save(article)

# 3. API Layer
@app.get("/api/articles/{id}")
async def get_article(id: str, repo: ArticleRepository = Depends(get_repo)):
    return repo.find_by_id(id)
```

**Impact:** HIGH - Maintainability, testability, scalability
**Complexity:** HIGH - Major refactoring

---

### **BP #8: No Rate Limiting di API**
**Priority:** 🔴 HIGH  
**Effort:** 1 day

**Problem:**
- API bisa di-spam unlimited
- No protection against DDoS
- Server bisa overload

**Solution:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/scrape")
@limiter.limit("5/minute")  # Max 5 requests per minute
async def scrape(request: Request, ...):
    ...

@app.get("/api/articles")
@limiter.limit("100/hour")  # Max 100 per hour
async def get_articles(request: Request, ...):
    ...
```

**Impact:** HIGH - Security, stability
**Complexity:** LOW - Library available

---

### **BP #9: Response Time Tidak Di-Track**
**Priority:** 🟠 MEDIUM-HIGH  
**Effort:** 0.5 day

**Problem:**
- Tidak tahu endpoint mana yang lambat
- No performance metrics
- No monitoring

**Solution:**
```python
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path}: {process_time:.3f}s")
    
    # Alert if slow
    if process_time > 5.0:
        logger.warning(f"SLOW REQUEST: {request.url.path} took {process_time:.3f}s")
    
    return response
```

**Impact:** MEDIUM - Monitoring, optimization
**Complexity:** LOW - Simple middleware

---

### **BP #10: No Unit Tests**
**Priority:** 🔴 HIGH  
**Effort:** 5 days

**Problem:**
```bash
python -m pytest tests/
# Result: No module named pytest

# Tests exist tapi tidak di-run!
ls tests/unit/
# test_batch_scraping.py, test_quick.py
```

**Solution:**
```bash
# 1. Install pytest
pip install pytest pytest-asyncio pytest-cov pytest-mock

# 2. Write tests untuk setiap module
# tests/unit/test_database.py
def test_insert_article_with_null_id():
    with Database(':memory:') as db:
        article = {'id': None, 'title': 'Test', 'url': 'http://test.com'}
        assert db.insert_article(article) == True
        
        articles = db.search_articles()
        assert len(articles) == 1
        assert articles[0]['id'] is not None

# 3. Setup CI/CD
# .github/workflows/ci.yml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest --cov=src --cov-report=html
```

**Impact:** HIGH - Code quality, regression prevention
**Complexity:** HIGH - Comprehensive test suite needed

---

## 🟡 MEDIUM PRIORITY ISSUES (8 Total)

### **PERF #1: Endpoint Detection Sangat Lambat (11.7s)**
**Priority:** 🟡 MEDIUM  
**Effort:** 1 day

**Problem:**
```
First call: 11.752s - 18 endpoints
Second call (cached): 0.000s - 18 endpoints
```

**Solution:**
```python
# 1. Parallel regex matching
import asyncio
import re

async def match_pattern(pattern, scripts):
    matches = []
    for script in scripts:
        if re.search(pattern, script):
            matches.append(...)
    return matches

# Run all patterns in parallel
tasks = [match_pattern(p, scripts) for p in patterns]
results = await asyncio.gather(*tasks)

# 2. Limit script tags to parse (top 10 only)
scripts = soup.find_all('script')[:10]  # Not all 50!

# 3. Cache per domain (already implemented)
```

**Impact:** MEDIUM - User experience
**Complexity:** MEDIUM - Async refactor

---

### **PERF #2: 21 Database Files (2.8MB)**
**Priority:** 🟡 MEDIUM  
**Effort:** 0.25 day

**Problem:**
```bash
ls data/*.db | wc -l
# 21 files!

# Files:
- comprehensive_full_test.db
- test_conn_0.db ... test_conn_9.db (10 files!)
- test_race.db, test_null.db, test_context.db, etc.
```

**Solution:**
```bash
# 1. Cleanup script
cat > cleanup_test_dbs.sh << 'SCRIPT'
#!/bin/bash
cd data/
# Keep only production DB
rm -f test_*.db tmp_*.db *_test.db
echo "Cleaned up test databases"
SCRIPT

# 2. Use in-memory DB for tests
# pytest conftest.py
@pytest.fixture
def test_db():
    db = Database(':memory:')  # In-memory!
    yield db
    db.close()
```

**Impact:** LOW - Disk space, organization
**Complexity:** LOW - Simple cleanup

---

### **PERF #3: No Index untuk Search**
**Priority:** 🟡 MEDIUM  
**Effort:** 0.5 day

**Problem:**
```sql
-- LIKE query tanpa index
SELECT * FROM articles WHERE title LIKE '%Kapolri%'
-- Full table scan!
```

**Solution:**
```sql
-- Full-text search index
CREATE VIRTUAL TABLE articles_fts USING fts5(
    title, 
    description, 
    content,
    content=articles,
    content_rowid=id
);

-- Populate FTS table
INSERT INTO articles_fts(rowid, title, description, content)
SELECT rowid, title, description, content FROM articles;

-- Search dengan FTS (MUCH faster)
SELECT * FROM articles 
WHERE id IN (
    SELECT rowid FROM articles_fts 
    WHERE articles_fts MATCH 'Kapolri'
);
```

**Impact:** MEDIUM - Search performance
**Complexity:** MEDIUM - FTS setup

---

### **PERF #4-8: Minor Performance Issues**

**4. Inefficient Tags Loading (Already Fixed!)**
✅ Fixed dengan bulk loading

**5. No Connection Pooling**
**Effort:** 1 day
```python
from sqlalchemy import create_engine, pool

engine = create_engine(
    'sqlite:///data/scraper.db',
    poolclass=pool.QueuePool,
    pool_size=5,
    max_overflow=10
)
```

**6. No Query Batching**
**Effort:** 1 day
```python
# Instead of:
for article in articles:
    db.insert_article(article)  # N queries

# Use:
db.insert_batch(articles)  # 1 transaction
```

**7. Large JSON in Metadata**
**Effort:** 0.5 day
```python
# Don't store raw_data in DB
# Only store essential metadata
metadata = {
    'source_api': article.get('source_api'),
    'scraped_from': article.get('scraped_from')
}
# raw_data di-exclude
```

**8. No Compression**
**Effort:** 0.25 day
```bash
# Compress database periodically
sqlite3 scraper.db "VACUUM;"
```

---

## 📅 SPRINT ROADMAP (3 Sprints)

### **SPRINT 2: High Priority Fixes (2 minggu)**
**Goal:** Fix semua HIGH priority issues

**Week 1:**
- ✅ Day 1-2: Complete logging migration (BP #1) - 80 prints remaining
- ✅ Day 3: Dependency injection untuk DB (BP #2)
- ✅ Day 4: Environment variables untuk config (BP #3)
- ✅ Day 5: Input validation (BP #4)

**Week 2:**
- ✅ Day 6: Async error handling (BP #5)
- ✅ Day 7: Cache expiration (BP #6)
- ✅ Day 8-9: Rate limiting (BP #8)
- ✅ Day 10: Response time tracking (BP #9)

**Deliverables:**
- All print statements → logger
- Dependency injection implemented
- Input validation on all endpoints
- Rate limiting active
- Performance monitoring

---

### **SPRINT 3: Architecture & Testing (2 minggu)**
**Goal:** Repository pattern + comprehensive tests

**Week 1:**
- ✅ Day 1-3: Implement repository pattern (BP #7)
- ✅ Day 4-5: Refactor API layer

**Week 2:**
- ✅ Day 6-8: Write unit tests (BP #10)
- ✅ Day 9: Setup CI/CD
- ✅ Day 10: Integration tests

**Deliverables:**
- Repository pattern implemented
- 80%+ test coverage
- CI/CD pipeline active
- All tests passing

---

### **SPRINT 4: Performance & Polish (1 minggu)**
**Goal:** Optimize performance issues

**Week 1:**
- ✅ Day 1: FTS search index (PERF #3)
- ✅ Day 2: Optimize endpoint detection (PERF #1)
- ✅ Day 3: Connection pooling (PERF #5)
- ✅ Day 4: Query batching (PERF #6)
- ✅ Day 5: Cleanup & documentation

**Deliverables:**
- Fast search (FTS)
- Optimized endpoint detection
- Connection pooling
- Single production database
- Complete documentation

---

## 📊 EFFORT ESTIMATION

### **By Priority:**
```
🔴 HIGH (10 issues):      12.5 days
🟡 MEDIUM (8 issues):     4.5 days
──────────────────────
TOTAL:                    17 days (~3.5 weeks)
```

### **By Category:**
```
Logging Migration:        2-3 days
Architecture:             4 days
Error Handling:           2 days
Performance:              3 days
Testing:                  5 days
Misc (rate limit, etc):   1.5 days
──────────────────────
TOTAL:                    17.5 days
```

### **By Sprint:**
```
Sprint 2 (HIGH):          10 days (2 weeks)
Sprint 3 (Architecture):  10 days (2 weeks)
Sprint 4 (Performance):   5 days (1 week)
──────────────────────
TOTAL:                    25 days (5 weeks)
```

---

## 🎯 PRIORITIZATION MATRIX

```
Impact vs Effort Matrix:

HIGH IMPACT, LOW EFFORT (Do First):
  1. ✅ Logging migration (partial done)
  2. ✅ Environment variables
  3. ✅ Cache expiration
  4. ✅ Rate limiting
  5. ✅ Response time tracking

HIGH IMPACT, MEDIUM EFFORT:
  6. ✅ Input validation
  7. ✅ Async error handling
  8. ✅ Dependency injection

HIGH IMPACT, HIGH EFFORT:
  9. ✅ Repository pattern
  10. ✅ Unit tests

MEDIUM IMPACT, LOW EFFORT (Quick wins):
  11. ✅ Cleanup test DBs
  12. ✅ Database compression

MEDIUM IMPACT, MEDIUM EFFORT:
  13. ✅ FTS search
  14. ✅ Optimize endpoint detection
  15. ✅ Connection pooling
```

---

## 💰 COST-BENEFIT ANALYSIS

### **High ROI (Return on Investment):**
1. **Logging System** - Already 50% done, high value
2. **Input Validation** - Prevents security issues
3. **Rate Limiting** - Protects server
4. **Unit Tests** - Prevents regressions

### **Medium ROI:**
5. **Repository Pattern** - Better architecture but big refactor
6. **FTS Search** - Nice to have but current search works
7. **Connection Pooling** - Helps at scale

### **Low ROI (Nice to have):**
8. **Cleanup DBs** - Minimal impact
9. **Compression** - Small space savings
10. **Optimize endpoint detection** - Already cached

---

## 📋 IMPLEMENTATION CHECKLIST

### **Before Starting Sprint 2:**
- [ ] Review current codebase
- [ ] Setup development branch
- [ ] Backup production database
- [ ] Install additional dependencies
- [ ] Setup testing environment

### **Dependencies to Install:**
```bash
pip install \
  pytest pytest-asyncio pytest-cov pytest-mock \
  slowapi \
  python-dotenv \
  sqlalchemy
```

### **Configuration Files to Create:**
```
.env                    # Environment variables
.env.example            # Template
pytest.ini              # Pytest config
.github/workflows/ci.yml  # CI/CD
```

---

## 🚦 DECISION POINTS

### **Option A: Sequential (Recommended)**
- Complete Sprint 2 fully
- Then Sprint 3
- Then Sprint 4
- **Duration:** 5 weeks
- **Risk:** LOW
- **Quality:** HIGH

### **Option B: Parallel (Aggressive)**
- Start Sprint 2 & 3 together
- Different team members
- **Duration:** 3 weeks
- **Risk:** MEDIUM
- **Quality:** MEDIUM

### **Option C: Cherry-Pick (Pragmatic)**
- Only fix critical HIGHs from Sprint 2
- Skip architecture refactor (Sprint 3)
- Basic tests only
- **Duration:** 2 weeks
- **Risk:** MEDIUM
- **Quality:** MEDIUM-LOW

---

## 🎓 RECOMMENDATIONS

### **Short Term (This Month):**
1. ✅ Complete logging migration
2. ✅ Add input validation
3. ✅ Implement rate limiting
4. ✅ Add basic error handling

### **Medium Term (Next Month):**
5. ✅ Repository pattern
6. ✅ Unit tests (80% coverage)
7. ✅ CI/CD setup

### **Long Term (Future):**
8. ✅ Full FTS search
9. ✅ Connection pooling
10. ✅ Performance optimization

---

## 📞 NEXT ACTIONS

**Immediate (Today):**
1. Review this roadmap
2. Prioritize which issues to fix first
3. Decide: Sequential vs Parallel vs Cherry-Pick

**This Week:**
4. Setup development environment
5. Create feature branches
6. Start Sprint 2

**This Month:**
7. Complete Sprint 2
8. Start Sprint 3

---

## ✅ SUCCESS CRITERIA

**Sprint 2 Success:**
- [ ] 0 print statements remaining (all → logger)
- [ ] All API endpoints have input validation
- [ ] Rate limiting active (5 req/min on /scrape)
- [ ] Response time tracking on all endpoints
- [ ] No global DB instance

**Sprint 3 Success:**
- [ ] Repository pattern implemented
- [ ] 80%+ test coverage
- [ ] CI/CD pipeline green
- [ ] All tests passing

**Sprint 4 Success:**
- [ ] Search < 100ms (FTS)
- [ ] Endpoint detection < 5s
- [ ] Single production DB
- [ ] Complete documentation

---

**Total Remaining Work:** 18 issues (10 HIGH + 8 MEDIUM)  
**Estimated Duration:** 5 weeks (3 sprints)  
**Current Progress:** 31% (8/26 fixed)  
**Target:** 100% (all 26 fixed)

---

*Roadmap Created: 24 Maret 2026*  
*Next Review: After Sprint 2*
