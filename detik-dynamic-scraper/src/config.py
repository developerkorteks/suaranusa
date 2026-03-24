"""
Configuration Management
Loads settings from environment variables with sensible defaults.

Author: Dynamic Scraper
Date: 2026-03-24
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "data/scraper.db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", ":memory:")

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Scraping
    RATE_LIMIT: float = float(os.getenv("RATE_LIMIT", "1.0"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "5"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/scraper.log")

    # Cache
    CACHE_TTL_HOURS: int = int(os.getenv("CACHE_TTL_HOURS", "1"))
    MAX_CACHE_SIZE: int = int(os.getenv("MAX_CACHE_SIZE", "10000"))

    @classmethod
    def get_database_url(cls, test_mode: bool = False) -> str:
        """Get database URL based on mode."""
        return cls.TEST_DATABASE_URL if test_mode else cls.DATABASE_URL


# Global settings instance
settings = Settings()


if __name__ == "__main__":
    print("Configuration loaded:")
    print(f"  DATABASE_URL: {settings.DATABASE_URL}")
    print(f"  API_HOST: {settings.API_HOST}")
    print(f"  API_PORT: {settings.API_PORT}")
    print(f"  RATE_LIMIT: {settings.RATE_LIMIT}")
    print(f"  LOG_LEVEL: {settings.LOG_LEVEL}")
    print(f"  CACHE_TTL_HOURS: {settings.CACHE_TTL_HOURS}")
