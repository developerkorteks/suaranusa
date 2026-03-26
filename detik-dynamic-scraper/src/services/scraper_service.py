"""
Scraper Service
Business logic for scraping operations.

Coordinates scraping, normalization, and storage.

Author: Dynamic Scraper
Date: 2026-03-24
"""

from typing import Dict, List, Optional, Any
import json
import asyncio
from repositories.article_repository import ArticleRepository
from core.content_scraper import ContentScraper
from core.article_detail_scraper import ArticleDetailScraper
from core.data_normalizer import DataNormalizer
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ScraperService:
    """
    Service for scraping-related business logic.

    Orchestrates scraping, normalization, and storage operations.
    """

    def __init__(
        self,
        repository: ArticleRepository,
        scraper: ContentScraper = None,
        normalizer: DataNormalizer = None,
    ):
        """
        Initialize scraper service.

        Args:
            repository: Article repository
            scraper: Content scraper (optional)
            normalizer: Data normalizer (optional)
        """
        self.repository = repository
        self.scraper = scraper or ContentScraper()
        self.normalizer = normalizer or DataNormalizer()

    async def scrape_and_save(
        self, url: str, response_type: str = "auto", normalize: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape URL and save articles to database.

        Args:
            url: URL to scrape
            response_type: Response type (auto/json/html)
            normalize: Whether to normalize data

        Returns:
            Result dict with success status and counts
        """
        try:
            # Scrape
            logger.info(f"Scraping {url}")
            articles = await self.scraper.scrape(url, response_type)

            if not articles:
                logger.warning(f"No articles found at {url}")
                return {
                    "success": True,
                    "articles_scraped": 0,
                    "articles_saved": 0,
                    "url": url,
                }

            # Normalize if requested
            if normalize:
                articles = self.normalizer.normalize_batch(articles, source=url)

            # Save to database
            saved_count = self.repository.save_batch(articles)

            logger.info(f"Scraped {len(articles)} articles, saved {saved_count}")

            return {
                "success": True,
                "articles_scraped": len(articles),
                "articles_saved": saved_count,
                "url": url,
            }

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}", exc_info=True)
            return {"success": False, "error": str(e), "url": url}

    async def scrape_only(
        self, url: str, response_type: str = "auto", normalize: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Scrape URL without saving (returns articles).

        Args:
            url: URL to scrape
            response_type: Response type
            normalize: Whether to normalize

        Returns:
            List of articles
        """
        try:
            articles = await self.scraper.scrape(url, response_type)

            if normalize:
                articles = self.normalizer.normalize_batch(articles, source=url)

            return articles

        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return []

    async def update_articles_media_batch(
        self,
        filters: Optional[Dict] = None,
        limit: Optional[int] = 10,
        skip_existing: bool = True,
        rate_limit: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Batch update media for existing articles.

        Args:
            filters: Filter dictionary (source, category)
            limit: Maximum articles to process
            skip_existing: Skip articles already having media
            rate_limit: Delay between requests

        Returns:
            Statistics dictionary
        """
        stats = {
            "total": 0,
            "processed": 0,
            "updated": 0,
            "failed": 0,
            "skipped": 0,
            "images_found": 0,
            "videos_found": 0,
        }

        # Get articles from repository
        query_params = filters or {}
        query_params["limit"] = limit or 1000

        articles = self.repository.search(**query_params)
        stats["total"] = len(articles)

        logger.info(f"Starting batch media update for {stats['total']} articles")

        detail_scraper = ArticleDetailScraper(rate_limit=rate_limit)

        for article in articles:
            is_success, media_info = await self._update_single_article_media(
                article, detail_scraper, skip_existing
            )

            if is_success:
                stats["updated"] += 1
                stats["images_found"] += media_info.get("images", 0)
                stats["videos_found"] += media_info.get("videos", 0)
            elif media_info.get("skipped"):
                stats["skipped"] += 1
            else:
                stats["failed"] += 1

            stats["processed"] += 1

            if stats["processed"] % 10 == 0:
                logger.info(f"Progress: {stats['processed']}/{stats['total']}")

        logger.info(
            f"Batch media update complete: {stats['updated']} updated, {stats['failed']} failed"
        )
        return stats

    async def _update_single_article_media(
        self,
        article: Dict[str, Any],
        detail_scraper: ArticleDetailScraper,
        skip_existing: bool,
    ) -> tuple:
        """Helper to update media for a single article."""
        article_id = article.get("id")
        url = article.get("url")

        if not url:
            return False, {"skipped": False}

        # Check if already has media
        metadata = article.get("metadata")
        if skip_existing and metadata:
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}

            if metadata.get("has_media") and metadata.get("images"):
                return False, {"skipped": True}

        try:
            article_data = await detail_scraper.scrape_article_detail(url)

            if not article_data:
                return False, {"skipped": False}

            images = article_data.get("images", [])
            videos = article_data.get("videos", [])

            if not images and not videos:
                return False, {"skipped": True}

            # Prepare update data
            update_data = {
                "id": article_id,
                "url": url,
                "title": article.get("title"),  # PRESERVE TITLE
                "source": article.get("source"),
                "category": article.get("category"),
                "image": article.get("image"),
                "publish_date": article.get("publish_date"),
                "description": article.get("description"),
                "metadata": article_data.get("metadata"),
                "images": images,
                "videos": videos,
                "has_media": True,
            }

            # Preserve/Update content
            if not article_data.get("content") and article.get("content"):
                update_data["content"] = article.get("content")
            else:
                update_data["content"] = article_data.get("content")

            # Preserve/Update author
            update_data["author"] = article_data.get("author") or article.get("author")
            # Preserve quality score
            update_data["quality_score"] = article.get("quality_score")

            # NEW: Run through normalizer to fix category and source consistency
            normalized = self.normalizer.normalize(update_data, source=update_data.get("source"))
            if normalized:
                update_data = normalized

            is_success = self.repository.save(update_data)
            return is_success, {"images": len(images), "videos": len(videos)}

        except Exception as e:
            logger.error(f"Error updating media for {article_id}: {e}")
            return False, {"skipped": False}
