# 📖 Complete API Usage Guide

**Detik Dynamic Scraper REST API**  
**Base URL:** `http://localhost:8000`  
**Documentation:** `http://localhost:8000/docs` (Swagger UI)  

---

## 🚀 Quick Start

### 1. Start the API Server

```bash
cd detik-dynamic-scraper
source ../venv_detik/bin/activate
python3 -m uvicorn src.api.main:app --reload
```

Server will be available at: **http://localhost:8000**

### 2. View Interactive Documentation

Open browser: **http://localhost:8000/docs**

---

## 📊 Complete API Flow

### Flow 1: Scrape Metadata Only (Current)

```
1. Discover domains
   POST /api/discover-domains
   
2. Detect endpoints
   POST /api/detect-endpoints
   
3. Scrape articles (metadata)
   POST /api/scrape
   
4. View in database
   POST /api/articles/search
   
5. Display in simple page
   Open: simple_article_page.html
```

### Flow 2: Scrape with Full Content (Future)

```
1. Same as Flow 1 steps 1-3
   
2. For each article, scrape detail:
   (Manual or batch process)
   
3. View full content
   GET /api/articles/{id}
```

---

## 🔗 API Endpoints

### 1. Health & Info

#### GET /
Get API information

**Response:**
```json
{
  "name": "Detik Dynamic Scraper API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": { ... }
}
```

#### GET /health
Health check

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-03-24T00:00:00",
  "database": "connected"
}
```

---

### 2. Discovery Operations

#### POST /api/discover-domains
Discover all subdomains

**Request:**
```json
{
  "base_url": "https://www.detik.com"
}
```

**Response:**
```json
{
  "success": true,
  "total_domains": 30,
  "domains": [
    "20.detik.com",
    "news.detik.com",
    ...
  ],
  "categories": {
    "content": [...],
    "api": [...],
    "services": [...]
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/discover-domains \
  -H "Content-Type: application/json" \
  -d '{"base_url": "https://www.detik.com"}'
```

---

#### POST /api/detect-endpoints
Detect API endpoints from domain

**Request:**
```json
{
  "domain": "news.detik.com"
}
```

**Response:**
```json
{
  "success": true,
  "domain": "news.detik.com",
  "total_endpoints": 18,
  "endpoints": [
    "https://recg.detik.com/article-recommendation/wp/...",
    ...
  ],
  "categories": {
    "recommendation": [...],
    "authentication": [...],
    ...
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/detect-endpoints \
  -H "Content-Type: application/json" \
  -d '{"domain": "news.detik.com"}'
```

---

### 3. Scraping Operations

#### POST /api/scrape
Scrape content from URL

**Request:**
```json
{
  "url": "https://news.detik.com",
  "response_type": "auto",
  "normalize": true,
  "save_to_db": true
}
```

**Parameters:**
- `url` (required): URL to scrape
- `response_type`: "auto", "json", or "html" (default: "auto")
- `normalize`: Apply data normalization (default: true)
- `save_to_db`: Save to database (default: true)

**Response:**
```json
{
  "success": true,
  "articles_count": 56,
  "articles": [
    {
      "id": "8412424",
      "title": "Article Title",
      "url": "https://...",
      "description": "...",
      "image": "https://...",
      "source": "news.detik.com",
      "quality_score": 0.85,
      "tags": ["tag1", "tag2"],
      ...
    }
  ],
  "timestamp": "2026-03-24T00:00:00"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.detik.com",
    "normalize": true,
    "save_to_db": true
  }'
```

---

### 4. Article Management

#### POST /api/articles/search
Search articles in database

**Request:**
```json
{
  "query": "keyword",
  "source": "news.detik.com",
  "category": "news",
  "limit": 100,
  "offset": 0
}
```

**Parameters (all optional):**
- `query`: Search keyword
- `source`: Filter by source domain
- `category`: Filter by category
- `limit`: Max results (default: 100)
- `offset`: Pagination offset (default: 0)

**Response:**
```json
{
  "success": true,
  "total": 56,
  "articles": [...],
  "filters": {
    "query": "keyword",
    "source": "news.detik.com",
    "category": "news"
  },
  "pagination": {
    "limit": 100,
    "offset": 0
  }
}
```

**Examples:**
```bash
# Get all articles
curl -X POST http://localhost:8000/api/articles/search \
  -H "Content-Type: application/json" \
  -d '{"limit": 50}'

# Search by keyword
curl -X POST http://localhost:8000/api/articles/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Iran", "limit": 10}'

# Filter by source
curl -X POST http://localhost:8000/api/articles/search \
  -H "Content-Type: application/json" \
  -d '{"source": "news.detik.com", "limit": 20}'
```

---

#### GET /api/articles/{article_id}
Get specific article by ID

**Example:**
```bash
curl http://localhost:8000/api/articles/8412424
```

**Response:**
```json
{
  "success": true,
  "article": {
    "id": "8412424",
    "title": "...",
    "content": "...",  // May be null if not scraped
    "url": "...",
    ...
  }
}
```

---

### 5. Statistics

#### GET /api/statistics
Get scraping statistics

**Response:**
```json
{
  "success": true,
  "database": {
    "total_articles": 538,
    "by_source": {
      "news.detik.com": 56,
      "finance.detik.com": 54,
      ...
    },
    "by_category": {...},
    "average_quality_score": 0.48,
    "total_tags": 102
  },
  "normalizer": {
    "total_processed": 538,
    "total_normalized": 538,
    "success_rate": 1.0,
    "average_quality_score": 0.48
  }
}
```

**Example:**
```bash
curl http://localhost:8000/api/statistics
```

---

### 6. Export

#### POST /api/export
Export articles to JSON file

**Parameters (query string):**
- `output_file`: Output file path (default: "data/export.json")
- `source`: Filter by source
- `category`: Filter by category
- `limit`: Max articles (default: 10000)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/export?output_file=data/my_export.json&limit=100"
```

**Response:**
```json
{
  "success": true,
  "exported_count": 538,
  "output_file": "data/my_export.json",
  "filters": {...}
}
```

---

### 7. Database Management

#### DELETE /api/articles
Clear all articles from database

**⚠️ Warning:** This will delete all data!

**Example:**
```bash
curl -X DELETE http://localhost:8000/api/articles
```

---

## 🌐 Consuming the API

### Method 1: Simple HTML Page (Provided)

**File:** `simple_article_page.html`

**Usage:**
1. Start API server
2. Open `simple_article_page.html` in browser
3. Articles load automatically from API

**Features:**
- Real-time data from API
- Search functionality
- Statistics display
- Click to open original article

---

### Method 2: JavaScript/Frontend

```javascript
// Fetch articles
async function getArticles() {
    const response = await fetch('http://localhost:8000/api/articles/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            limit: 50
        })
    });
    
    const data = await response.json();
    return data.articles;
}

// Use the data
getArticles().then(articles => {
    articles.forEach(article => {
        console.log(article.title);
    });
});
```

---

### Method 3: Python Script

```python
import requests

# Get articles
response = requests.post(
    'http://localhost:8000/api/articles/search',
    json={'limit': 50}
)

articles = response.json()['articles']

for article in articles:
    print(f"{article['title']} - {article['url']}")
```

---

### Method 4: cURL (Command Line)

```bash
# Get statistics
curl http://localhost:8000/api/statistics | jq

# Search articles
curl -X POST http://localhost:8000/api/articles/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Iran", "limit": 10}' | jq

# Trigger scraping
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.detik.com",
    "save_to_db": true
  }' | jq '.articles_count'
```

---

## 📱 Complete Usage Example

### Scenario: Scrape and Display Articles

**Step 1: Start API**
```bash
cd detik-dynamic-scraper
python3 -m uvicorn src.api.main:app --reload
```

**Step 2: Trigger Scraping**
```bash
curl -X POST http://localhost:8000/api/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.detik.com",
    "normalize": true,
    "save_to_db": true
  }'
```

**Step 3: View Statistics**
```bash
curl http://localhost:8000/api/statistics | jq '.database.total_articles'
```

**Step 4: Display in Browser**
- Open `simple_article_page.html` in browser
- Articles display automatically

**Step 5: Search Articles**
- Type in search box
- Results filter in real-time

---

## 🎯 Integration Examples

### React/Next.js

```javascript
// hooks/useArticles.js
import { useState, useEffect } from 'react';

export function useArticles(limit = 50) {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetch('http://localhost:8000/api/articles/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ limit })
        })
        .then(r => r.json())
        .then(data => {
            setArticles(data.articles);
            setLoading(false);
        });
    }, [limit]);
    
    return { articles, loading };
}

// Component
function ArticlesList() {
    const { articles, loading } = useArticles();
    
    if (loading) return <div>Loading...</div>;
    
    return (
        <div>
            {articles.map(article => (
                <ArticleCard key={article.id} article={article} />
            ))}
        </div>
    );
}
```

---

### Vue.js

```javascript
// ArticlesList.vue
<template>
    <div>
        <div v-for="article in articles" :key="article.id">
            <h2>{{ article.title }}</h2>
            <p>{{ article.description }}</p>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            articles: []
        }
    },
    async mounted() {
        const response = await fetch('http://localhost:8000/api/articles/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ limit: 50 })
        });
        const data = await response.json();
        this.articles = data.articles;
    }
}
</script>
```

---

## 🔒 CORS Configuration

If accessing API from different domain, ensure CORS is enabled:

```python
# In src/api/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify domains
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Response Formats

### Success Response
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

---

## 🎯 Best Practices

1. **Rate Limiting:** Don't spam API, respect delays
2. **Error Handling:** Always check `success` field
3. **Pagination:** Use `limit` and `offset` for large datasets
4. **Caching:** Cache results when appropriate
5. **HTTPS:** Use HTTPS in production

---

## 📚 Additional Resources

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Dashboard:** http://localhost:8501
- **Simple Page:** simple_article_page.html

---

**API Version:** 1.0  
**Last Updated:** 2026-03-24  
**Status:** Production Ready  

🎉 **Ready to use!**
