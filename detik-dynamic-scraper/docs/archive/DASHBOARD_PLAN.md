# 📊 Streamlit Dashboard Implementation Plan

**Date:** 2026-03-24  
**Objective:** Create visual dashboard for Detik Dynamic Scraper  
**Framework:** Streamlit  
**Approach:** Step-by-step with incremental testing  

---

## 🎯 DASHBOARD REQUIREMENTS

### Must Have:
1. ✅ Real-time statistics display
2. ✅ Article browser/search
3. ✅ Scraping controls (trigger scraping)
4. ✅ Domain & endpoint discovery
5. ✅ Export functionality

### Nice to Have:
6. 📊 Charts (articles by domain, quality distribution)
7. 🔍 Advanced filters
8. 📈 Real-time progress monitoring
9. ⚙️ Configuration settings

---

## 📋 IMPLEMENTATION STEPS

### Step 1: Setup & Dependencies
**File:** `requirements.txt` (update)  
**Tasks:**
- Add streamlit
- Add plotly (for charts)
- Add pandas (for data manipulation)

**Test:**
- Install dependencies
- Import streamlit successfully

**Expected:** No errors, all imports working

---

### Step 2: Basic Dashboard Layout
**File:** `dashboard.py`  
**Tasks:**
- Create page layout (sidebar + main)
- Add title and header
- Add navigation menu
- Setup multi-page structure

**Test:**
- Run `streamlit run dashboard.py`
- See basic layout
- Navigation working

**Expected:** Dashboard opens, shows title and sidebar

---

### Step 3: Statistics Page
**File:** `pages/1_📊_Statistics.py`  
**Tasks:**
- Fetch data from database
- Display key metrics (cards)
- Show articles by domain (bar chart)
- Show quality distribution (histogram)
- Show source breakdown (pie chart)

**Test:**
- Navigate to Statistics page
- See all metrics and charts
- Data updates correctly

**Expected:** Beautiful statistics visualization

---

### Step 4: Article Browser
**File:** `pages/2_📰_Articles.py`  
**Tasks:**
- Display articles in table/cards
- Add search functionality
- Add filters (category, source, date)
- Add pagination
- Show article details on click

**Test:**
- Browse articles
- Search works
- Filters work
- Pagination works

**Expected:** Easy article browsing and search

---

### Step 5: Scraping Controls
**File:** `pages/3_🚀_Scraper.py`  
**Tasks:**
- Domain discovery button
- Endpoint detection selector
- Scrape trigger with parameters
- Progress bar
- Real-time status updates

**Test:**
- Trigger domain discovery
- Select domain and detect endpoints
- Start scraping
- See progress

**Expected:** Can trigger scraping from dashboard

---

### Step 6: Configuration & Settings
**File:** `pages/4_⚙️_Settings.py`  
**Tasks:**
- Database path configuration
- Rate limit settings
- Max workers configuration
- Export options

**Test:**
- Change settings
- Settings persist
- Apply to scraper

**Expected:** Configurable scraper settings

---

## 🧪 TESTING STRATEGY

### After Each Step:
```bash
streamlit run dashboard.py
```

### Validation Checklist:
- [ ] Page loads without errors
- [ ] UI elements visible
- [ ] Data fetches correctly
- [ ] Interactions work
- [ ] No console errors

---

## 📊 DASHBOARD STRUCTURE

```
dashboard.py                    # Main entry point
├── pages/
│   ├── 1_📊_Statistics.py     # Statistics & charts
│   ├── 2_📰_Articles.py        # Article browser
│   ├── 3_🚀_Scraper.py         # Scraping controls
│   └── 4_⚙️_Settings.py        # Configuration
└── utils/
    ├── db_helper.py            # Database utilities
    └── api_helper.py           # API client
```

---

## 🎨 UI MOCKUP

```
╔═══════════════════════════════════════════════════════════════╗
║  🕷️ Detik Dynamic Scraper Dashboard                          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌─ Sidebar ─┐  ┌─ Main Content ──────────────────────────┐ ║
║  │ 📊 Stats   │  │                                         │ ║
║  │ 📰 Articles│  │  📊 Key Metrics                         │ ║
║  │ 🚀 Scraper │  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │ ║
║  │ ⚙️ Settings│  │  │ 538 │ │ 20  │ │0.48 │ │ 102 │       │ ║
║  │            │  │  │Arts │ │Doms │ │Qual │ │Tags │       │ ║
║  │            │  │  └─────┘ └─────┘ └─────┘ └─────┘       │ ║
║  │            │  │                                         │ ║
║  │            │  │  📈 Charts                              │ ║
║  │            │  │  [Bar Chart: Articles by Domain]       │ ║
║  │            │  │  [Pie Chart: Sources]                  │ ║
║  │            │  │  [Histogram: Quality Distribution]     │ ║
║  │            │  │                                         │ ║
║  └────────────┘  └─────────────────────────────────────────┘ ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 📝 CODE STRUCTURE

### Main Dashboard (dashboard.py):
```python
import streamlit as st

st.set_page_config(
    page_title="Detik Dynamic Scraper",
    page_icon="🕷️",
    layout="wide"
)

st.title("🕷️ Detik Dynamic Scraper Dashboard")
st.markdown("Real-time monitoring and control")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    # Auto navigation by Streamlit pages/
```

### Statistics Page (pages/1_📊_Statistics.py):
```python
import streamlit as st
import plotly.express as px
from utils.db_helper import get_statistics

st.title("📊 Statistics")

# Fetch data
stats = get_statistics()

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Articles", stats['total_articles'])
col2.metric("Domains", len(stats['by_source']))
col3.metric("Avg Quality", f"{stats['average_quality_score']:.2f}")
col4.metric("Tags", stats['total_tags'])

# Charts
fig = px.bar(data, x='domain', y='count')
st.plotly_chart(fig)
```

---

## ✅ SUCCESS CRITERIA

### After Each Step:
- [ ] No errors in console
- [ ] UI renders correctly
- [ ] Data displays accurately
- [ ] Interactions work smoothly

### Final Dashboard:
- [ ] All 4 pages working
- [ ] Statistics display correctly
- [ ] Article browser functional
- [ ] Scraping can be triggered
- [ ] Settings can be changed
- [ ] Responsive design
- [ ] Professional appearance

---

## 🎯 DELIVERABLES

1. **dashboard.py** - Main entry point
2. **pages/1_📊_Statistics.py** - Statistics page
3. **pages/2_📰_Articles.py** - Article browser
4. **pages/3_🚀_Scraper.py** - Scraping controls
5. **pages/4_⚙️_Settings.py** - Configuration
6. **utils/db_helper.py** - Database utilities
7. **utils/api_helper.py** - API client
8. **requirements.txt** - Updated dependencies

---

## ⏱️ TIME ESTIMATE

- Step 1: Setup - 2 minutes
- Step 2: Layout - 3 minutes
- Step 3: Statistics - 5 minutes
- Step 4: Articles - 4 minutes
- Step 5: Scraper - 3 minutes
- Step 6: Settings - 2 minutes
- **Total: ~20 minutes**

---

**Ready to implement Step 1: Setup & Dependencies** ✅
