"""
REST API - Refactored for Service Layer

FastAPI-based REST API for the dynamic scraper.

Author: Dynamic Scraper
Date: 2026-03-24
"""

from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.database import Database
from repositories.article_repository import ArticleRepository
from services.article_service import ArticleService
from services.scraper_service import ScraperService
from services.sync_service import SyncService
from core.data_normalizer import DataNormalizer
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

# BP #8: Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Initialize FastAPI app
app = FastAPI(
    title="Detik Dynamic Scraper API",
    description="REST API for dynamic web scraping system",
    version="1.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiter setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Response time middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# Global Service Instances
SCRAPER_ROOT = Path(__file__).parent.parent.parent
DEFAULT_DB_PATH = SCRAPER_ROOT / "data" / "comprehensive_full_test.db"

# BP #7: Environment-based configuration
import os
from dotenv import load_dotenv
load_dotenv(SCRAPER_ROOT / ".env")

DB_PATH = os.getenv("DATABASE_PATH", str(DEFAULT_DB_PATH))
logger.info(f"Using database at: {DB_PATH}")

db_instance = Database(DB_PATH)
article_repo = ArticleRepository(db_instance)
article_service = ArticleService(article_repo)
scraper_service = ScraperService(article_repo)
sync_service = SyncService(article_repo, scraper_service)


# Pydantic Models
class ScrapeRequest(BaseModel):
    url: str
    response_type: str = "auto"
    normalize: bool = True
    save_to_db: bool = True


class SearchRequest(BaseModel):
    query: Optional[str] = None
    source: Optional[str] = None
    category: Optional[str] = None
    limit: int = 100
    offset: int = 0


class SyncRequest(BaseModel):
    articles_per_domain: int = 20


class BatchMediaUpdateRequest(BaseModel):
    source: Optional[str] = None
    category: Optional[str] = None
    limit: Optional[int] = 10
    skip_existing: bool = True
    rate_limit: float = 2.0


# Routes
@app.get("/")
async def root():
    return {"name": "Detik Scraper API", "version": "1.1.0", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy", "database": "connected"}


@app.post("/api/scrape")
async def scrape(request: ScrapeRequest):
    try:
        result = await scraper_service.scrape_and_save(
            request.url, request.response_type, request.normalize
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sync/full")
async def sync_full(request: SyncRequest):
    """Trigger a full production sync cycle across discovered subdomains."""
    try:
        # Run in background to avoid timeout
        asyncio.create_task(sync_service.run_full_sync(request.articles_per_domain))
        return {
            "success": True,
            "message": "Full sync started in background",
            "articles_per_domain": request.articles_per_domain,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/articles/search")
async def search_articles(request: SearchRequest):
    try:
        articles = article_service.search_articles(
            query=request.query,
            source=request.source,
            category=request.category,
            limit=request.limit,
            offset=request.offset,
        )
        return {"success": True, "total": len(articles), "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/{article_id}")
async def get_article(article_id: str):
    article = article_service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"success": True, "article": article}


@app.post("/api/articles/{article_id}/scrape-detail")
async def scrape_article_detail(article_id: str):
    # For now, we reuse existing logic but could move to service
    article = article_service.get_article(article_id)
    if not article or not article.get("url"):
        raise HTTPException(status_code=404, detail="Article URL not found")

    from core.article_detail_scraper import ArticleDetailScraper

    detail_scraper = ArticleDetailScraper(rate_limit=0.5)
    detail_data = await detail_scraper.scrape_article_detail(article["url"])

    if detail_data:
        detail_data["id"] = article_id
        article_service.save_article(detail_data)

        content = detail_data.get("content") or ""
        return {
            "success": True,
            "article_id": article_id,
            "content_length": len(content),
            "has_content": bool(content),
            "author": detail_data.get("author"),
            "timestamp": datetime.utcnow().isoformat(),
        }

    raise HTTPException(status_code=500, detail="Failed to scrape detail")


@app.post("/api/articles/batch-update-media")
async def batch_update_media(request: BatchMediaUpdateRequest):
    """Trigger batch media update process."""
    try:
        filters = {}
        if request.source:
            filters["source"] = request.source
        if request.category:
            filters["category"] = request.category

        stats = await scraper_service.update_articles_media_batch(
            filters=filters,
            limit=request.limit,
            skip_existing=request.skip_existing,
            rate_limit=request.rate_limit,
        )
        return {"success": True, "stats": stats}
    except Exception as e:
        logger.error(f"Batch update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/statistics")
async def get_statistics():
    return {"success": True, "statistics": article_service.get_statistics()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
