"""
Repositories Package
Data access layer following Repository Pattern.

Author: Dynamic Scraper
Date: 2026-03-24
"""

from .article_repository import ArticleRepository
from .base_repository import BaseRepository

__all__ = ["ArticleRepository", "BaseRepository"]
