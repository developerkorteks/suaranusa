"""
Sync Service - Production Orchestrator
Handles fully automated background synchronization.
"""

import asyncio
import time
from typing import Dict, Any, List
from repositories.article_repository import ArticleRepository
from services.scraper_service import ScraperService
from core.domain_discovery import DomainDiscovery
from core.content_scraper import ContentScraper
from core.article_detail_scraper import ArticleDetailScraper
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SyncService:
    def __init__(self, repository: ArticleRepository, scraper_service: ScraperService):
        self.repository = repository
        self.scraper_service = scraper_service
        self.discovery = DomainDiscovery()
        self.list_scraper = ContentScraper()
        self.detail_scraper = ArticleDetailScraper(rate_limit=0.2)

    async def run_full_sync(self, articles_per_domain: int = 20):
        """
        Executes a complete production sync cycle:
        1. Discover Subdomains
        2. Scrape Latest Articles (List)
        3. Hydrate Full Content & Media (Detail)
        """
        logger.info("Starting Full Production Sync Cycle...")
        start_time = time.time()

        # Step 1: Discover Domains
        domains = await self.discovery.discover()
        content_domains = [
            d
            for d in sorted(domains)
            if "detik.com" in d
            and not any(x in d for x in ["cdn", "static", "api", "analytic"])
        ]

        logger.info(
            f"Step 1 Complete: Found {len(content_domains)} domains to process."
        )

        # Step 2: Scrape Lists and Step 3: Hydrate Details
        total_synced = 0
        for domain in content_domains:
            logger.info(f"Processing Domain: {domain}")
            try:
                # Scrape List
                target_url = f"https://{domain}"
                articles = await self.list_scraper.scrape(target_url)
                
                if not articles:
                    continue
                    
                targets = articles[:articles_per_domain]

                # Immediate Hydration (Auto-Hydration with Media)
                for article in targets:
                    url = article.get("url")
                    if not url:
                        continue
                    
                    # Ensure article has a clean source for the normalizer
                    article["source"] = domain

                    # FIX: Use detail_scraper instead of list_scraper for media hydration
                    success, media_info = (
                        await self.scraper_service._update_single_article_media(
                            article, self.detail_scraper, skip_existing=True
                        )
                    )
                    if success:
                        total_synced += 1
                        logger.info(f"  ✓ Hydrated: {article.get('title')[:50]}... (Images: {media_info.get('images', 0)})")

            except Exception as e:
                logger.error(f"Error syncing domain {domain}: {e}")

        duration = time.time() - start_time
        logger.info(f"Full Sync Complete! Total articles hydrated: {total_synced}")
        logger.info(f"Total Duration: {duration/60:.2f} minutes")

        return {
            "total_hydrated": total_synced,
            "duration_seconds": duration,
            "domains_processed": len(content_domains),
        }
