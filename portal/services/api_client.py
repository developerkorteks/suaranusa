import httpx
import logging
from django.conf import settings
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ApiService:
    """
    Service to handle all communication with the FastAPI Backend.
    Fixes 'Event loop is closed' by using request-scoped clients.
    """
    
    def _get_client(self) -> httpx.AsyncClient:
        """Helper to create a configured client."""
        return httpx.AsyncClient(
            base_url=settings.API_BASE_URL,
            timeout=30.0,
            headers={"Content-Type": "application/json"}
        )

    async def get_articles(self, limit: int = 20, offset: int = 0, source: Optional[str] = None, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """Fetch articles from the API with source filter, pagination and SEARCH."""
        try:
            async with self._get_client() as client:
                payload = {"limit": limit, "offset": offset}
                if source: payload["source"] = source
                if query: payload["query"] = query
                
                response = await client.post("/api/articles/search", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("articles", [])
        except Exception as e:
            logger.error(f"API ERROR [get_articles]: {e}")
            return []

    async def get_article_detail(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single article detail by ID."""
        try:
            async with self._get_client() as client:
                # Clean ID from any potential prefixes if accidentally passed
                clean_id = str(article_id).replace('d-', '')
                response = await client.get(f"/api/articles/{clean_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    article = data.get("article")
                    if article:
                        return article
                logger.warning(f"API Returned {response.status_code} for article {article_id}")
            return None
        except Exception as e:
            logger.error(f"API ERROR [get_article_detail] for ID {article_id}: {e}")
            return None

    async def trigger_scrape_detail(self, article_id: str) -> bool:
        """Force the API to scrape full content/media for an article."""
        try:
            async with self._get_client() as client:
                clean_id = str(article_id).replace('d-', '')
                response = await client.post(f"/api/articles/{clean_id}/scrape-detail")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"API ERROR [trigger_scrape_detail] for {article_id}: {e}")
            return False

    async def trigger_global_scrape(self, url: str) -> bool:
        """Trigger a global scrape for a domain."""
        try:
            async with self._get_client() as client:
                response = await client.post("/api/scrape", json={"url": url})
                return response.status_code == 200
        except Exception as e:
            logger.error(f"API ERROR [trigger_global_scrape] for {url}: {e}")
            return False
