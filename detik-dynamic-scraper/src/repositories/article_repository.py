"""
Article Repository
Handles all database operations for articles.

Implements Repository Pattern to separate data access from business logic.

Author: Dynamic Scraper
Date: 2026-03-24
"""

from typing import Dict, List, Optional, Any
from .base_repository import BaseRepository
from storage.database import Database
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ArticleRepository(BaseRepository):
    """
    Repository for Article entity.

    Handles all CRUD operations and queries related to articles.
    Encapsulates database access logic.
    """

    def __init__(self, db: Database):
        """Initialize article repository."""
        super().__init__(db)

    def find_by_id(self, article_id: str) -> Optional[Dict[str, Any]]:
        """
        Find article by ID.

        Args:
            article_id: Article identifier

        Returns:
            Article dict or None if not found
        """
        try:
            return self.db.get_article(article_id)
        except Exception as e:
            logger.error(f"Error finding article {article_id}: {e}")
            return None

    def find_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Find all articles with pagination.

        Args:
            limit: Maximum results
            offset: Pagination offset

        Returns:
            List of article dicts
        """
        try:
            return self.db.search_articles(limit=limit, offset=offset)
        except Exception as e:
            logger.error(f"Error finding articles: {e}")
            return []

    def save(self, article: Dict[str, Any]) -> bool:
        """
        Save article (insert or update).

        Args:
            article: Article data

        Returns:
            True if successful
        """
        try:
            return self.db.insert_article(article)
        except Exception as e:
            logger.error(f"Error saving article: {e}")
            return False

    def save_batch(self, articles: List[Dict[str, Any]]) -> int:
        """
        Save multiple articles.

        Args:
            articles: List of article data

        Returns:
            Number of successfully saved articles
        """
        try:
            return self.db.insert_batch(articles)
        except Exception as e:
            logger.error(f"Error saving batch: {e}")
            return 0

    def delete(self, article_id: str) -> bool:
        """
        Delete article by ID.

        Args:
            article_id: Article identifier

        Returns:
            True if successful
        """
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            self.db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting article {article_id}: {e}")
            return False

    def search(
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
        try:
            return self.db.search_articles(
                query=query,
                source=source,
                category=category,
                limit=limit,
                offset=offset,
            )
        except Exception as e:
            logger.error(f"Error searching articles: {e}")
            return []

    def get_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Find article by URL.

        Args:
            url: Article URL

        Returns:
            Article dict or None
        """
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE url = ?", (url,))
            row = cursor.fetchone()

            if row:
                article = dict(row)
                article["tags"] = self.db._get_article_tags(article["id"])
                return article
            return None
        except Exception as e:
            logger.error(f"Error finding article by URL: {e}")
            return None

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get article statistics.

        Returns:
            Statistics dict
        """
        try:
            return self.db.get_statistics()
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}

    def clear_all(self) -> bool:
        """
        Clear all articles (use with caution!).

        Returns:
            True if successful
        """
        try:
            self.db.clear_all()
            logger.warning("All articles cleared from database")
            return True
        except Exception as e:
            logger.error(f"Error clearing articles: {e}")
            return False

    def export_to_json(self, output_file: str, filters: Optional[Dict] = None) -> int:
        """
        Export articles to JSON file.

        Args:
            output_file: Output file path
            filters: Optional filters

        Returns:
            Number of exported articles
        """
        try:
            return self.db.export_to_json(output_file, filters)
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return 0

    def count(self) -> int:
        """
        Count total articles.

        Returns:
            Total number of articles
        """
        try:
            stats = self.db.get_statistics()
            return stats.get("total_articles", 0)
        except Exception as e:
            logger.error(f"Error counting articles: {e}")
            return 0
