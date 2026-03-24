"""
Article Service
Business logic for article operations.

Coordinates between repositories and implements business rules.

Author: Dynamic Scraper
Date: 2026-03-24
"""

from typing import Dict, List, Optional, Any
from repositories.article_repository import ArticleRepository
from core.data_normalizer import DataNormalizer
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ArticleService:
    """
    Service for article-related business logic.

    Coordinates between repository, normalizer, and implements
    business rules for article operations.
    """

    def __init__(
        self, repository: ArticleRepository, normalizer: DataNormalizer = None
    ):
        """
        Initialize article service.

        Args:
            repository: Article repository
            normalizer: Data normalizer (optional)
        """
        self.repository = repository
        self.normalizer = normalizer or DataNormalizer()

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        """
        Get article by ID.

        Args:
            article_id: Article identifier

        Returns:
            Article data or None
        """
        return self.repository.find_by_id(article_id)

    def get_articles(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Get all articles with pagination.

        Args:
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of articles
        """
        return self.repository.find_all(limit=limit, offset=offset)

    def search_articles(
        self,
        query: Optional[str] = None,
        source: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Search articles with filters.

        Args:
            query: Search query
            source: Filter by source
            category: Filter by category
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of matching articles
        """
        return self.repository.search(
            query=query, source=source, category=category, limit=limit, offset=offset
        )

    def save_article(self, article: Dict[str, Any], normalize: bool = True) -> bool:
        """
        Save article with optional normalization.

        Args:
            article: Article data
            normalize: Whether to normalize before saving

        Returns:
            True if successful
        """
        if normalize:
            # Normalize article data
            normalized = self.normalizer.normalize(
                article, source=article.get("source_url", "unknown")
            )
            if not normalized:
                logger.warning("Article failed normalization, skipping")
                return False
            article = normalized

        return self.repository.save(article)

    def save_articles_batch(
        self, articles: List[Dict[str, Any]], normalize: bool = True
    ) -> int:
        """
        Save multiple articles.

        Args:
            articles: List of article data
            normalize: Whether to normalize before saving

        Returns:
            Number of successfully saved articles
        """
        if normalize:
            # Normalize all articles
            normalized_articles = self.normalizer.normalize_batch(
                articles,
                source=(
                    articles[0].get("source_url", "unknown") if articles else "unknown"
                ),
            )
            articles = normalized_articles

        return self.repository.save_batch(articles)

    def delete_article(self, article_id: str) -> bool:
        """
        Delete article by ID.

        Args:
            article_id: Article identifier

        Returns:
            True if successful
        """
        return self.repository.delete(article_id)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get article statistics.

        Returns:
            Statistics dict
        """
        return self.repository.get_statistics()

    def export_articles(self, output_file: str, filters: Optional[Dict] = None) -> int:
        """
        Export articles to JSON file.

        Args:
            output_file: Output file path
            filters: Optional filters

        Returns:
            Number of exported articles
        """
        return self.repository.export_to_json(output_file, filters)

    def article_exists(self, article_id: str) -> bool:
        """
        Check if article exists.

        Args:
            article_id: Article identifier

        Returns:
            True if exists
        """
        return self.repository.exists(article_id)

    def get_article_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Find article by URL.

        Args:
            url: Article URL

        Returns:
            Article data or None
        """
        return self.repository.get_by_url(url)

    def clear_all_articles(self) -> bool:
        """
        Clear all articles (use with caution!).

        Returns:
            True if successful
        """
        logger.warning("Clearing all articles from database")
        return self.repository.clear_all()
