"""
Comprehensive Scraper - Scrape ALL Detik Subdomains

Implements comprehensive scraping strategy:
- All 32+ subdomains
- Multiple API endpoints per domain
- Homepage + API scraping
- Parallel execution

Author: Dynamic Scraper
Date: 2026-03-23
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
import os

# FIX BUG #8: Add proper logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.logger import setup_logger

from .content_scraper import ContentScraper
from .parameter_extractor import ParameterExtractor
from .data_normalizer import DataNormalizer
from .domain_discovery import DomainDiscovery
from .endpoint_detector import EndpointDetector

logger = setup_logger(__name__)


class ComprehensiveScraper:
    """Scrape all Detik subdomains comprehensively - FULLY DYNAMIC."""

    # REMOVED: ALL_SUBDOMAINS hardcoded list
    # Now uses DomainDiscovery to find domains dynamically

    # REMOVED: API_ENDPOINTS hardcoded dict
    # Now uses EndpointDetector to detect endpoints dynamically

    # Terpopuler URLs
    TERPOPULER_URLS = [
        "https://www.detik.com/terpopuler",
        "https://www.detik.com/terpopuler/1",
        "https://www.detik.com/terpopuler/3",
        "https://www.detik.com/terpopuler/7",
        "https://www.detik.com/terpopuler/30",
    ]

    def __init__(self, rate_limit: float = 1.0, max_workers: int = 5):
        """
        Initialize comprehensive scraper - FULLY DYNAMIC.

        Args:
            rate_limit: Delay between requests
            max_workers: Maximum parallel workers
        """
        self.scraper = ContentScraper(rate_limit=rate_limit)
        self.extractor = ParameterExtractor()
        self.normalizer = DataNormalizer()
        self.discovery = DomainDiscovery()  # NEW: Dynamic discovery
        self.detector = EndpointDetector()  # NEW: Dynamic endpoint detection
        self.max_workers = max_workers
        self._endpoint_cache = {}  # Cache detected endpoints per domain

        self.results = {
            "by_subdomain": {},
            "by_endpoint": {},
            "terpopuler": [],
            "total_articles": 0,
            "scraped_at": datetime.utcnow().isoformat(),
        }

    async def _discover_domains(self) -> set:
        """
        Dynamically discover all domains.

        Returns:
            Set of discovered domain names
        """
        print("🔍 Discovering domains dynamically...")
        domains = await self.discovery.discover()
        logger.info(f"Discovered {len(domains)} domains")
        return domains

    async def scrape_all_subdomains(
        self,
        subdomain_list: Optional[List[str]] = None,
        articles_per_subdomain: int = 30,
    ) -> Dict[str, Any]:
        """
        Scrape all subdomains - FULLY DYNAMIC.

        Args:
            subdomain_list: Optional list (default: auto-discover)
            articles_per_subdomain: Target articles per subdomain

        Returns:
            Dictionary with scraping results
        """
        # STEP 1: Dynamic discovery (if no list provided)
        if subdomain_list is None:
            discovered = await self._discover_domains()
            # Filter to content channels only (exclude API/service domains)
            subdomains = sorted(
                [
                    d
                    for d in discovered
                    if not any(
                        x in d
                        for x in [
                            "recg.",
                            "rech.",
                            "cdn",
                            "analytic",
                            "adsmart",
                            "apicomment",
                            "connect.",
                            "newrevive",
                            "rekomendit",
                        ]
                    )
                ]
            )
        else:
            subdomains = subdomain_list

        logger.info(f"Starting comprehensive scrape of {len(subdomains)} subdomains")
        logger.info(f"Target: {articles_per_subdomain} articles per subdomain")
        logger.info(f"Max workers: {self.max_workers}")
        pass  # Empty line removed

        # Create tasks for all subdomains
        tasks = []
        for subdomain in subdomains:
            task = self._scrape_subdomain(subdomain, articles_per_subdomain)
            tasks.append(task)

        # Execute with semaphore to limit concurrency
        semaphore = asyncio.Semaphore(self.max_workers)

        async def limited_scrape(task):
            async with semaphore:
                return await task

        # Run all tasks
        results = await asyncio.gather(
            *[limited_scrape(t) for t in tasks], return_exceptions=True
        )

        # Process results
        for subdomain, result in zip(subdomains, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to scrape {subdomain}: {result}")
                self.results["by_subdomain"][subdomain] = {
                    "error": str(result),
                    "articles": [],
                }
            else:
                self.results["by_subdomain"][subdomain] = result
                self.results["total_articles"] += len(result.get("articles", []))

        return self.results

    async def _scrape_subdomain(
        self, subdomain: str, target_articles: int
    ) -> Dict[str, Any]:
        """Scrape a single subdomain using multiple strategies."""
        result = {
            "subdomain": subdomain,
            "articles": [],
            "sources": [],
        }

        logger.info(f"Scraping {subdomain}...")

        # Strategy 1: Homepage scraping
        try:
            homepage_articles = await self.scraper.scrape(
                subdomain, response_type="html"
            )
            if homepage_articles:
                result["articles"].extend(homepage_articles)
                result["sources"].append("homepage")
                logger.info(
                    f"Homepage: {len(homepage_articles)} articles from {subdomain}"
                )
        except Exception as e:
            logger.warning(f"Homepage scraping failed for {subdomain}: {e}")

        # Strategy 2: API endpoints (if not enough articles)
        if len(result["articles"]) < target_articles:
            remaining = target_articles - len(result["articles"])
            api_articles = await self._scrape_api_endpoints(subdomain, remaining)
            if api_articles:
                result["articles"].extend(api_articles)
                result["sources"].append("api")
                logger.info(f"API: {len(api_articles)} articles from {subdomain}")

        # Normalize all articles
        if result["articles"]:
            normalized = self.normalizer.normalize_batch(result["articles"], subdomain)
            result["articles"] = normalized
            logger.info(f"Total: {len(normalized)} articles from {subdomain}")

        return result

    async def _detect_endpoints(self, domain: str) -> set:
        """
        Dynamically detect endpoints for a domain.

        Args:
            domain: Domain to detect endpoints from

        Returns:
            Set of detected endpoint URLs
        """
        # Check cache first
        if domain in self._endpoint_cache:
            return self._endpoint_cache[domain]

        # Detect endpoints
        endpoints = await self.detector.detect(domain)

        # Cache for reuse
        self._endpoint_cache[domain] = endpoints

        return endpoints

    async def _scrape_api_endpoints(
        self, subdomain: str, count: int
    ) -> List[Dict[str, Any]]:
        """Scrape API endpoints for a subdomain - FULLY DYNAMIC."""
        articles = []

        # Get acctype for this subdomain
        params = await self.extractor.extract(subdomain, "")
        acctype = params.get("acctype", "acc-detikcom")

        # STEP 2: Dynamic endpoint detection
        # Try to detect from a main domain (use news.detik.com as reference)
        detected_endpoints = await self._detect_endpoints("news.detik.com")

        # Filter for recommendation endpoints
        recommendation_endpoints = [
            ep
            for ep in detected_endpoints
            if "article-recommendation" in str(ep) and "recg" in str(ep)
        ]

        # Try detected endpoints
        for endpoint in recommendation_endpoints[:2]:  # Try first 2
            if len(articles) >= count:
                break

            try:
                # Build URL with parameters
                url = str(endpoint)
                # Add query parameters if not present
                if "?" not in url:
                    url += f"test?size={min(count - len(articles), 30)}&nocache=1&ids=undefined&acctype={acctype}"

                result = await self.scraper.scrape(url, response_type="json")
                articles.extend(result)
            except Exception as e:
                pass  # Silent fail, try next endpoint

        return articles

    async def scrape_terpopuler(self) -> List[Dict[str, Any]]:
        """Scrape all Terpopuler pages."""
        print("\n📈 Scraping Terpopuler pages...")

        all_articles = []

        for url in self.TERPOPULER_URLS:
            try:
                articles = await self.scraper.scrape(url, response_type="html")
                if articles:
                    normalized = self.normalizer.normalize_batch(articles, "terpopuler")
                    all_articles.extend(normalized)
                    print(
                        f"  ✅ {url.split('/')[-1] or 'all'}: {len(normalized)} articles"
                    )
            except Exception as e:
                logger.warning(f"Failed scraping {url}: {e}")

        self.results["terpopuler"] = all_articles
        return all_articles

    def get_statistics(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        stats = {
            "total_subdomains_scraped": len(self.results["by_subdomain"]),
            "total_articles": self.results["total_articles"],
            "total_terpopuler": len(self.results["terpopuler"]),
            "by_subdomain_count": {
                subdomain: len(data.get("articles", []))
                for subdomain, data in self.results["by_subdomain"].items()
            },
            "normalizer_stats": self.normalizer.get_stats(),
        }
        return stats


if __name__ == "__main__":
    # Quick test
    import asyncio

    async def test():
        print("🧪 Testing Comprehensive Scraper")
        print("=" * 60)

        scraper = ComprehensiveScraper(rate_limit=0.5, max_workers=3)

        # Test with subset of subdomains
        test_subdomains = [
            "news.detik.com",
            "finance.detik.com",
            "sport.detik.com",
        ]

        results = await scraper.scrape_all_subdomains(
            test_subdomains, articles_per_subdomain=10
        )

        print("\n" + "=" * 60)
        print("📊 Results:")

        stats = scraper.get_statistics()
        print(f"  - Subdomains scraped: {stats['total_subdomains_scraped']}")
        print(f"  - Total articles: {stats['total_articles']}")
        print(f"  - Per subdomain: {stats['by_subdomain_count']}")

        print("\n✅ Test complete!")

    asyncio.run(test())
