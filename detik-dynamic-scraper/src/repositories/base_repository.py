"""
Base Repository
Abstract base class for all repositories.

Provides common CRUD operations and database connection management.

Author: Dynamic Scraper
Date: 2026-03-24
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from storage.database import Database


class BaseRepository(ABC):
    """
    Base repository with common database operations.

    All repositories should inherit from this class and implement
    their specific business logic while leveraging common operations.
    """

    def __init__(self, db: Database):
        """
        Initialize repository with database connection.

        Args:
            db: Database instance (injected)
        """
        self.db = db

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Find entity by ID."""
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Find all entities with pagination."""
        pass

    @abstractmethod
    def save(self, entity: Dict[str, Any]) -> bool:
        """Save entity (insert or update)."""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """Delete entity by ID."""
        pass

    def exists(self, id: str) -> bool:
        """Check if entity exists."""
        return self.find_by_id(id) is not None

    def count(self) -> int:
        """Count total entities."""
        # Subclasses can override with specific implementation
        return len(self.find_all(limit=999999))
