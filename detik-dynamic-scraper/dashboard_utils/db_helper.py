"""Smart Database Wrapper for Dashboard Compatibility."""

import sys
from pathlib import Path

# Add root and src to path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path / "src"))

from storage.database import Database
from config import settings

# Singleton-like database instance for the dashboard
_db = None


def get_db(db_path=None):
    """Get or create database connection."""
    global _db
    if _db is None:
        path = db_path or "data/comprehensive_full_test.db"
        _db = Database(path)
    return _db


def get_statistics():
    """Get statistics via Database."""
    return get_db().get_statistics()


def search_articles(query=None, source=None, category=None, limit=100, offset=0):
    """Search articles via Database."""
    return get_db().search_articles(
        query=query, source=source, category=category, limit=limit, offset=offset
    )


def get_article(article_id):
    """Get article by ID via Database."""
    return get_db().get_article(article_id)


def close_db():
    """Close the database connection."""
    global _db
    if _db is not None:
        _db.close()
        _db = None
