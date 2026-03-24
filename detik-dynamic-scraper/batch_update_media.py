#!/usr/bin/env python3
"""
Batch Re-scrape Script - Update Media for Existing Articles

This script re-scrapes existing articles in the database to extract and update
their media (images and videos).

Usage:
    python batch_update_media.py --limit 10
    python batch_update_media.py --source hot.detik.com
    python batch_update_media.py --all
"""

import asyncio
import argparse
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.article_detail_scraper import ArticleDetailScraper
from storage.database import Database
import json


class BatchMediaUpdater:
    """Batch update media for existing articles."""

    def __init__(self, db_path="data/comprehensive_full_test.db", rate_limit=2.0):
        """
        Initialize batch updater.

        Args:
            db_path: Database path
            rate_limit: Delay between requests (seconds)
        """
        self.db = Database(db_path)
        self.scraper = ArticleDetailScraper(rate_limit=rate_limit)
        self.stats = {
            "total": 0,
            "processed": 0,
            "updated": 0,
            "failed": 0,
            "skipped": 0,
            "images_found": 0,
            "videos_found": 0,
        }

    async def update_article_media(self, article):
        """
        Update media for a single article.

        Args:
            article: Article dict from database

        Returns:
            True if updated, False otherwise
        """
        article_id = article.get("id")
        url = article.get("url")

        print(
            f"\n[{self.stats['processed'] + 1}/{self.stats['total']}] Processing: {article_id}"
        )
        print(f"   URL: {url}")

        # Check if already has media
        metadata = article.get("metadata")
        if metadata:
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}

            if metadata.get("has_media") and metadata.get("images"):
                print(f"   ⏭️  Already has media, skipping...")
                self.stats["skipped"] += 1
                return False

        # Scrape article detail
        try:
            article_data = await self.scraper.scrape_article_detail(url)

            if not article_data:
                print(f"   ❌ Failed to scrape")
                self.stats["failed"] += 1
                return False

            # Check if media found
            images = article_data.get("images", [])
            videos = article_data.get("videos", [])

            if not images and not videos:
                print(f"   ⚠️  No media found")
                self.stats["skipped"] += 1
                return False

            print(f"   ✅ Found: {len(images)} images, {len(videos)} videos")

            # Update article in database
            article_data["id"] = article_id
            article_data["url"] = url
            article_data["source"] = article.get("source")

            # Preserve existing content if new scrape doesn't have it
            if not article_data.get("content") and article.get("content"):
                article_data["content"] = article.get("content")

            success = self.db.insert_article(article_data)

            if success:
                print(f"   💾 Updated in database")
                self.stats["updated"] += 1
                self.stats["images_found"] += len(images)
                self.stats["videos_found"] += len(videos)
                return True
            else:
                print(f"   ❌ Failed to update database")
                self.stats["failed"] += 1
                return False

        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.stats["failed"] += 1
            return False
        finally:
            self.stats["processed"] += 1

    async def batch_update(self, filters=None, limit=None, skip_existing=True):
        """
        Batch update articles.

        Args:
            filters: Dict with source, category filters
            limit: Max articles to process
            skip_existing: Skip articles that already have media
        """
        print("=" * 70)
        print("🔄 BATCH MEDIA UPDATE")
        print("=" * 70)

        # Get articles from database
        query_params = {
            "source": filters.get("source") if filters else None,
            "category": filters.get("category") if filters else None,
            "limit": limit or 1000,
        }

        articles = self.db.search_articles(**query_params)
        self.stats["total"] = len(articles)

        print(f"\nFound {self.stats['total']} articles to process")

        if filters:
            print(f"Filters: {filters}")

        print(f"Rate limit: {self.scraper.rate_limit}s per request")
        print(f"Skip existing: {skip_existing}")
        print("-" * 70)

        start_time = datetime.now()

        # Process articles
        for article in articles:
            await self.update_article_media(article)

            # Progress update every 10 articles
            if self.stats["processed"] % 10 == 0:
                self.print_progress()

        # Final summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 70)
        print("📊 BATCH UPDATE COMPLETE")
        print("=" * 70)
        print(f"\nTotal articles: {self.stats['total']}")
        print(f"Processed: {self.stats['processed']}")
        print(f"Updated: {self.stats['updated']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"\nMedia found:")
        print(f"  Images: {self.stats['images_found']}")
        print(f"  Videos: {self.stats['videos_found']}")
        print(f"\nTime: {duration:.1f}s ({duration/60:.1f} minutes)")
        print(f"Rate: {self.stats['processed']/duration*60:.1f} articles/minute")
        print("=" * 70)

        self.db.close()

    def print_progress(self):
        """Print progress update."""
        progress = (self.stats["processed"] / self.stats["total"]) * 100
        print(
            f"\n📊 Progress: {self.stats['processed']}/{self.stats['total']} ({progress:.1f}%)"
        )
        print(
            f"   Updated: {self.stats['updated']}, Skipped: {self.stats['skipped']}, Failed: {self.stats['failed']}"
        )


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Batch update media for existing articles"
    )
    parser.add_argument("--limit", type=int, help="Max articles to process")
    parser.add_argument("--source", type=str, help="Filter by source domain")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument(
        "--all", action="store_true", help="Process all articles (no limit)"
    )
    parser.add_argument(
        "--db",
        type=str,
        default="data/comprehensive_full_test.db",
        help="Database path",
    )
    parser.add_argument("--rate", type=float, default=2.0, help="Rate limit in seconds")

    args = parser.parse_args()

    # Build filters
    filters = {}
    if args.source:
        filters["source"] = args.source
    if args.category:
        filters["category"] = args.category

    # Determine limit
    limit = None
    if args.all:
        limit = None
    elif args.limit:
        limit = args.limit
    else:
        limit = 10  # Default

    # Create updater
    updater = BatchMediaUpdater(db_path=args.db, rate_limit=args.rate)

    # Run batch update
    await updater.batch_update(filters=filters or None, limit=limit)


if __name__ == "__main__":
    asyncio.run(main())
