"""
Domain Discovery System - Step 1
Auto-detect all detik.com subdomains dynamically
"""

import re
from typing import Set, List, Optional
from urllib.parse import urlparse
import httpx
from bs4 import BeautifulSoup
import sys
import os

# Add proper logging
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
# FIX: Dummy logger fallback for dashboard compatibility
try:
    from utils.logger import setup_logger

    logger = setup_logger(__name__)
except ImportError:

    class DummyLogger:
        def info(self, msg):
            print(f"INFO: {msg}")

        def warning(self, msg):
            print(f"WARNING: {msg}")

        def error(self, msg, exc_info=False):
            print(f"ERROR: {msg}")

        def debug(self, msg):
            pass

    logger = DummyLogger()


class DomainDiscovery:
    """Automatically discover Detik.com subdomains."""

    def __init__(self, base_domain: str = "detik.com"):
        self.base_domain = base_domain
        self.discovered_domains: Set[str] = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def discover(self) -> Set[str]:
        """
        Main discovery method - orchestrates all discovery techniques.

        Returns:
            Set[str]: Set of discovered subdomains
        """
        logger.info(" Starting domain discovery...")

        # Method 1: Parse main homepage
        await self._discover_from_homepage()

        # Method 2: Parse sitemap
        await self._discover_from_sitemap()

        # Method 3: Common subdomain enumeration
        await self._discover_common_subdomains()

        logger.info(" Discovered {len(self.discovered_domains)} unique domains")
        return self.discovered_domains

    async def _discover_from_homepage(self):
        """Extract subdomains from main homepage."""
        logger.info("  → Parsing homepage...")

        url = f"https://www.{self.base_domain}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=10.0)
                response.raise_for_status()

                html = response.text
                soup = BeautifulSoup(html, "lxml")

                # Find all links
                links = soup.find_all("a", href=True)

                for link in links:
                    href = link["href"]
                    domain = self._extract_subdomain(href)
                    if domain:
                        self.discovered_domains.add(domain)

                # Also check script tags and other sources
                for tag in soup.find_all(["script", "link", "img"]):
                    src = tag.get("src") or tag.get("href")
                    if src:
                        domain = self._extract_subdomain(src)
                        if domain:
                            self.discovered_domains.add(domain)

                logger.info(
                    f"    ✓ Found {len(self.discovered_domains)} domains from homepage"
                )

        except Exception as e:
            logger.info(f"    ✗ Error parsing homepage: {e}")

    async def _discover_from_sitemap(self):
        """Extract subdomains from sitemap.xml."""
        logger.info("  → Parsing sitemap...")

        sitemap_urls = [
            f"https://www.{self.base_domain}/sitemap.xml",
            f"https://www.{self.base_domain}/sitemap_index.xml",
        ]

        for sitemap_url in sitemap_urls:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        sitemap_url, headers=self.headers, timeout=10.0
                    )

                    if response.status_code == 200:
                        # Parse XML
                        soup = BeautifulSoup(response.text, "lxml")

                        # Find all <loc> tags
                        locs = soup.find_all("loc")

                        for loc in locs:
                            url = loc.get_text()
                            domain = self._extract_subdomain(url)
                            if domain:
                                self.discovered_domains.add(domain)

                        logger.info(f"    ✓ Found domains from sitemap: {sitemap_url}")
                        break  # Stop if one sitemap works

            except Exception as e:
                logger.info(f"    ⚠ Sitemap {sitemap_url} not accessible: {e}")
                continue

    async def _discover_common_subdomains(self):
        """Try common subdomain patterns."""
        logger.info("  → Checking common subdomains...")

        # Common subdomains based on our previous analysis
        common_subdomains = [
            "www",
            "news",
            "finance",
            "sport",
            "hot",
            "inet",
            "travel",
            "food",
            "health",
            "oto",
            "wolipop",
            "20",  # 20.detik.com for videos
            "foto",
            "event",
            "karir",
            # API subdomains
            "rech",
            "rech20",
            "recg",
            "connect",
            "apicomment",
            # Services
            "adsmart",
            "rekomendit",
            "pasangmata",
            "fyb",
            # CDN
            "cdn",
            "cdnv",
            "cdnstatic",
            "awscdn",
            # Other
            "analytic",
            "newrevive",
        ]

        async with httpx.AsyncClient() as client:
            for subdomain in common_subdomains:
                domain = f"{subdomain}.{self.base_domain}"

                # Quick check if domain is accessible
                try:
                    url = f"https://{domain}"
                    response = await client.head(
                        url, headers=self.headers, timeout=5.0, follow_redirects=True
                    )

                    if response.status_code < 500:  # Any response except server error
                        self.discovered_domains.add(domain)
                        logger.info(f"    ✓ Verified: {domain}")

                except Exception:
                    # Domain not accessible, skip silently
                    pass

    def _extract_subdomain(self, url: str) -> Optional[str]:
        """
        Extract subdomain from URL if it's a detik.com domain.

        Args:
            url: URL to parse

        Returns:
            Subdomain string or None
        """
        try:
            # Handle relative URLs
            if url.startswith("/"):
                return None

            # Handle protocol-relative URLs
            if url.startswith("//"):
                url = "https:" + url

            # Parse URL
            parsed = urlparse(url)
            hostname = parsed.hostname

            if not hostname:
                return None

            # Check if it's a detik domain
            if self.base_domain in hostname:
                # Return full subdomain (e.g., news.detik.com)
                return hostname

            return None

        except Exception:
            return None

    def get_domains_by_category(self) -> dict:
        """
        Categorize discovered domains.

        Returns:
            Dict with categorized domains
        """
        categories = {"content": [], "api": [], "cdn": [], "services": [], "other": []}

        # Categorization patterns
        content_patterns = [
            "news",
            "finance",
            "sport",
            "hot",
            "inet",
            "travel",
            "food",
            "health",
            "oto",
            "wolipop",
            "www",
            "20",
            "foto",
        ]
        api_patterns = ["rech", "recg", "api", "connect"]
        cdn_patterns = ["cdn", "aws", "static"]
        service_patterns = [
            "adsmart",
            "rekomendit",
            "pasangmata",
            "fyb",
            "event",
            "karir",
            "analytic",
        ]

        for domain in self.discovered_domains:
            categorized = False

            if any(pattern in domain for pattern in content_patterns):
                categories["content"].append(domain)
                categorized = True
            elif any(pattern in domain for pattern in api_patterns):
                categories["api"].append(domain)
                categorized = True
            elif any(pattern in domain for pattern in cdn_patterns):
                categories["cdn"].append(domain)
                categorized = True
            elif any(pattern in domain for pattern in service_patterns):
                categories["services"].append(domain)
                categorized = True

            if not categorized:
                categories["other"].append(domain)

        return categories


# Synchronous wrapper for testing
def discover_domains_sync(base_domain: str = "detik.com") -> Set[str]:
    """Synchronous wrapper for domain discovery."""
    import asyncio

    discovery = DomainDiscovery(base_domain)
    return asyncio.run(discovery.discover())
