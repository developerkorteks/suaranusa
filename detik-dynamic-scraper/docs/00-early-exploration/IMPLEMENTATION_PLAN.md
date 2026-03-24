# 🚀 Detik.com Fully Dynamic Scraping System - Implementation Plan

## 🎯 Project Goals

**Primary Objective:** Build a fully dynamic scraping system that automatically adapts to:
- New subdomains
- Changing API endpoints
- New content structures
- Different response formats

**Key Requirements:**
1. ✅ Fully dynamic (no hardcoded domains/endpoints)
2. ✅ Auto-discovery of new subdomains
3. ✅ Automatic API endpoint detection
4. ✅ Smart parameter extraction
5. ✅ Exclude ads, scrape everything else
6. ✅ REST API layer
7. ✅ Optional dashboard for manual domain input
8. ✅ Test every small step
9. ✅ Zero bugs, zero vulnerabilities
10. ✅ Production-ready code

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                           │
│  ┌──────────────┐           ┌──────────────┐              │
│  │  REST API    │           │  Dashboard   │ (Optional)   │
│  │  (FastAPI)   │           │  (Streamlit) │              │
│  └──────┬───────┘           └──────┬───────┘              │
└─────────┼──────────────────────────┼────────────────────────┘
          │                          │
          ▼                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Core Scraping Engine                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Domain Discovery Service                         │  │
│  │     - Auto-detect subdomains from main page          │  │
│  │     - DNS enumeration                                │  │
│  │     - Sitemap parsing                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  2. API Endpoint Detector                            │  │
│  │     - Analyze HTML for API calls                     │  │
│  │     - Extract XHR patterns                           │  │
│  │     - Discover hidden endpoints                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  3. Parameter Extractor                              │  │
│  │     - Auto-detect required parameters                │  │
│  │     - Extract from HTML meta tags                    │  │
│  │     - Learn from response headers                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  4. Content Scraper                                  │  │
│  │     - Smart HTML parsing                             │  │
│  │     - JSON API handling                              │  │
│  │     - Ad filtering                                   │  │
│  │     - Deduplication                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  5. Data Normalizer                                  │  │
│  │     - Unified output format                          │  │
│  │     - Schema validation                              │  │
│  │     - Data enrichment                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Storage Layer                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   SQLite     │  │    Redis     │  │     JSON     │     │
│  │  (Metadata)  │  │   (Cache)    │  │   (Export)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Implementation Steps (Small Increments)

### **Phase 1: Foundation (Steps 1-3)**

#### Step 1: Domain Discovery System
**Goal:** Auto-detect all detik.com subdomains dynamically

**Tasks:**
- [ ] 1.1: Parse main page for subdomain links
- [ ] 1.2: Extract from sitemap.xml
- [ ] 1.3: DNS enumeration (common subdomains)
- [ ] 1.4: Store discovered domains in DB
- [ ] 1.5: Test with known domains

**Test:**
```python
discovered = DomainDiscovery().discover()
assert 'news.detik.com' in discovered
assert 'finance.detik.com' in discovered
assert len(discovered) >= 20
```

---

#### Step 2: API Endpoint Auto-Detection
**Goal:** Automatically find API endpoints from any page

**Tasks:**
- [ ] 2.1: Parse HTML for script tags
- [ ] 2.2: Extract fetch/XMLHttpRequest calls
- [ ] 2.3: Analyze network waterfall simulation
- [ ] 2.4: Pattern matching for API URLs
- [ ] 2.5: Test endpoint validity
- [ ] 2.6: Store in endpoint registry

**Test:**
```python
endpoints = EndpointDetector().detect('news.detik.com')
assert any('recommendation' in e for e in endpoints)
assert any('comment' in e for e in endpoints)
```

---

#### Step 3: Dynamic Parameter Extraction
**Goal:** Auto-extract required parameters for each API

**Tasks:**
- [ ] 3.1: Analyze API call signatures
- [ ] 3.2: Extract from meta tags (clientId, acctype, etc)
- [ ] 3.3: Learn from successful requests
- [ ] 3.4: Build parameter schema per endpoint
- [ ] 3.5: Test parameter generation

**Test:**
```python
params = ParameterExtractor().extract('rech.detik.com', 'news')
assert 'acctype' in params
assert params['acctype'] == 'acc-detiknews'
assert 'size' in params
```

---

### **Phase 2: Core Scraping (Steps 4-5)**

#### Step 4: Content Scraper Engine
**Goal:** Scrape content from any discovered endpoint

**Tasks:**
- [ ] 4.1: Implement adaptive HTML parser
- [ ] 4.2: Implement JSON API handler
- [ ] 4.3: Build ad detection & filtering
- [ ] 4.4: Create deduplication logic
- [ ] 4.5: Error handling & retry logic
- [ ] 4.6: Rate limiting
- [ ] 4.7: Test with multiple domains

**Test:**
```python
scraper = DynamicScraper()
articles = scraper.scrape('news.detik.com')
assert len(articles) > 0
assert all('id' in a for a in articles)
assert all('title' in a for a in articles)
# Ensure no ads
assert not any('ad' in a.get('type', '') for a in articles)
```

---

#### Step 5: Data Normalizer
**Goal:** Unified output format regardless of source

**Tasks:**
- [ ] 5.1: Define universal schema
- [ ] 5.2: Create field mapping system
- [ ] 5.3: Implement data validators
- [ ] 5.4: Add enrichment (timestamps, source, etc)
- [ ] 5.5: Test with diverse sources

**Test:**
```python
raw_data = {...}  # From API
normalized = DataNormalizer().normalize(raw_data)
assert 'id' in normalized
assert 'title' in normalized
assert 'published_at' in normalized
assert 'source_url' in normalized
```

---

### **Phase 3: API Layer (Step 6)**

#### Step 6: FastAPI REST API
**Goal:** Expose scraping functionality via REST API

**Endpoints:**
```
GET  /api/v1/domains              - List all discovered domains
POST /api/v1/domains/discover     - Trigger domain discovery
GET  /api/v1/domains/{domain}/endpoints - List endpoints for domain
POST /api/v1/scrape               - Scrape specific domain/endpoint
GET  /api/v1/articles             - Get scraped articles
GET  /api/v1/health               - Health check
```

**Tasks:**
- [ ] 6.1: Setup FastAPI project
- [ ] 6.2: Create domain management endpoints
- [ ] 6.3: Create scraping endpoints
- [ ] 6.4: Add authentication (API key)
- [ ] 6.5: Add rate limiting
- [ ] 6.6: Add OpenAPI docs
- [ ] 6.7: Test all endpoints

**Test:**
```python
response = client.get('/api/v1/domains')
assert response.status_code == 200
assert len(response.json()) > 0

response = client.post('/api/v1/scrape', json={'domain': 'news.detik.com'})
assert response.status_code == 200
assert 'articles' in response.json()
```

---

### **Phase 4: Dashboard (Optional - Step 7)**

#### Step 7: Streamlit Dashboard
**Goal:** Web UI for manual domain management

**Features:**
- Domain discovery interface
- Manual domain input
- Real-time scraping status
- Data visualization
- Export functionality

**Tasks:**
- [ ] 7.1: Setup Streamlit app
- [ ] 7.2: Domain management UI
- [ ] 7.3: Scraping control panel
- [ ] 7.4: Results display
- [ ] 7.5: Export to CSV/JSON
- [ ] 7.6: Test UI flows

---

### **Phase 5: Testing & Deployment (Steps 8-9)**

#### Step 8: Comprehensive Testing
**Tasks:**
- [ ] 8.1: Unit tests (90%+ coverage)
- [ ] 8.2: Integration tests
- [ ] 8.3: End-to-end tests
- [ ] 8.4: Performance tests
- [ ] 8.5: Security audit
- [ ] 8.6: Bug fixes

#### Step 9: Production Deployment
**Tasks:**
- [ ] 9.1: Docker containerization
- [ ] 9.2: Environment configuration
- [ ] 9.3: Logging & monitoring
- [ ] 9.4: Deployment scripts
- [ ] 9.5: Documentation

---

## 🎨 Technology Stack

```
Core:
  - Python 3.11+
  - asyncio (async/await)
  
Web Scraping:
  - httpx (async HTTP)
  - BeautifulSoup4 (HTML parsing)
  - lxml (fast parsing)
  
API:
  - FastAPI (REST API)
  - Pydantic (validation)
  - uvicorn (ASGI server)
  
Storage:
  - SQLite (lightweight DB)
  - Redis (caching) - optional
  
Dashboard (Optional):
  - Streamlit (UI)
  
Testing:
  - pytest
  - pytest-asyncio
  - pytest-cov
  
Deployment:
  - Docker
  - Docker Compose
```

---

## 🔒 Security Considerations

1. **Input Validation**
   - Sanitize all user inputs
   - Validate domain formats
   - Prevent SSRF attacks

2. **Rate Limiting**
   - Per-domain rate limits
   - API endpoint rate limits
   - Prevent abuse

3. **Authentication**
   - API key for REST API
   - Token-based auth for dashboard

4. **Data Privacy**
   - No personal data storage
   - Comply with robots.txt
   - Respect rate limits

---

## 📊 Success Criteria

Each step must pass:
- ✅ All unit tests passing
- ✅ No bugs or errors
- ✅ Performance acceptable (<2s per page)
- ✅ Memory usage reasonable (<500MB)
- ✅ Clean code (pylint score >8.0)
- ✅ Documentation complete

---

## 🚦 Development Workflow

For each step:
1. **Plan** - Write specifications
2. **Implement** - Small, focused code
3. **Test** - Unit + integration tests
4. **Review** - Code review & refactor
5. **Commit** - Git commit with tests
6. **Document** - Update docs

**Rule:** Never move to next step until current step is 100% complete and tested.

---

## 📝 File Structure

```
detik-dynamic-scraper/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── domain_discovery.py      # Step 1
│   │   ├── endpoint_detector.py     # Step 2
│   │   ├── parameter_extractor.py   # Step 3
│   │   ├── scraper_engine.py        # Step 4
│   │   └── data_normalizer.py       # Step 5
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app
│   │   ├── routes/
│   │   └── models/
│   ├── dashboard/                   # Optional
│   │   └── app.py
│   └── utils/
│       ├── cache.py
│       ├── db.py
│       └── helpers.py
├── tests/
│   ├── test_domain_discovery.py
│   ├── test_endpoint_detector.py
│   ├── test_parameter_extractor.py
│   ├── test_scraper_engine.py
│   └── test_api.py
├── config/
│   └── settings.py
├── data/
│   ├── domains.db
│   └── cache/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🎯 Next Steps

**Start with Step 1: Domain Discovery System**
- Focus on small, testable increments
- Write tests first (TDD)
- Ensure 100% completion before moving forward

Ready to implement? Let's start! 🚀
