"""
API Endpoint Detector - Step 2
Auto-detect API endpoints from any domain dynamically
"""

import re
from typing import Set, List, Dict, Optional
from urllib.parse import urlparse, urljoin
import httpx
from bs4 import BeautifulSoup
import json
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


class EndpointDetector:
    """Automatically detect API endpoints from HTML pages."""

    def __init__(self):
        self.detected_endpoints: Set[str] = set()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    async def detect(self, domain: str) -> Set[str]:
        """
        Main detection method - find all API endpoints for a domain.

        Args:
            domain: Domain to analyze (e.g., 'news.detik.com')

        Returns:
            Set[str]: Set of discovered API endpoints
        """
        logger.info(" Detecting API endpoints for {domain}...")

        self.detected_endpoints.clear()

        # Method 1: Parse HTML for API calls
        await self._detect_from_html(domain)

        # Method 2: Extract from JavaScript
        await self._detect_from_javascript(domain)

        # Method 3: Pattern-based detection
        await self._detect_known_patterns(domain)

        logger.info(" Detected {len(self.detected_endpoints)} API endpoints")
        return self.detected_endpoints

    async def _detect_from_html(self, domain: str):
        """Extract API endpoints from HTML page source."""
        logger.info("  → Analyzing HTML...")

        url = f"https://{domain}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, headers=self.headers, timeout=15.0, follow_redirects=True
                )
                response.raise_for_status()

                html = response.text

                # Pattern 1: Look for https://*.detik.com/* in HTML
                url_pattern = r'https?://([a-z0-9\-]+\.detik\.[a-z\.]+)(/[^\s\'"<>]*)?'
                matches = re.findall(url_pattern, html, re.IGNORECASE)

                for match in matches:
                    full_domain = match[0]
                    path = match[1] if match[1] else ""

                    # Filter for API-like endpoints
                    if self._is_api_endpoint(full_domain, path):
                        endpoint = f"https://{full_domain}{path}"
                        self.detected_endpoints.add(endpoint)

                logger.info(
                    f"    ✓ Found {len(self.detected_endpoints)} endpoints from HTML"
                )

        except Exception as e:
            logger.info(f"    ✗ Error analyzing HTML: {e}")

    async def _detect_from_javascript(self, domain: str):
        """Extract API endpoints from JavaScript code."""
        logger.info("  → Analyzing JavaScript...")

        url = f"https://{domain}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, timeout=15.0)
                html = response.text
                soup = BeautifulSoup(html, "lxml")

                # Find all script tags
                scripts = soup.find_all("script")

                for script in scripts:
                    script_content = script.string
                    if not script_content:
                        continue

                    # Look for fetch(), XMLHttpRequest, $.ajax, etc.
                    api_patterns = [
                        r'fetch\([\'"]([^\'"]+)[\'"]',
                        r'XMLHttpRequest.*?open\([\'"]GET[\'"],\s*[\'"]([^\'"]+)[\'"]',
                        r'\$\.ajax\(\{[^\}]*url:\s*[\'"]([^\'"]+)[\'"]',
                        r'\$\.get\([\'"]([^\'"]+)[\'"]',
                        r'\$\.post\([\'"]([^\'"]+)[\'"]',
                    ]

                    for pattern in api_patterns:
                        matches = re.findall(pattern, script_content, re.IGNORECASE)
                        for match in matches:
                            # Clean up the URL
                            endpoint_url = match.strip()

                            # Make absolute URL
                            if endpoint_url.startswith("/"):
                                endpoint_url = f"https://{domain}{endpoint_url}"
                            elif not endpoint_url.startswith("http"):
                                continue

                            # Check if it's a detik domain
                            if "detik" in endpoint_url and self._is_api_endpoint(
                                endpoint_url, ""
                            ):
                                self.detected_endpoints.add(endpoint_url)

                logger.info(f"    ✓ Analyzed {len(scripts)} script tags")

        except Exception as e:
            logger.info(f"    ✗ Error analyzing JavaScript: {e}")

    async def _detect_known_patterns(self, domain: str):
        """Detect endpoints based on known patterns from our analysis."""
        logger.info("  → Checking known patterns...")

        # Based on our previous analysis, construct possible endpoints
        api_patterns = [
            # Recommendation APIs
            ("rech.detik.com", "/article-recommendation/detail/"),
            ("rech.detik.com", "/article-recommendation/wp/"),
            ("rech20.detik.com", "/article-recommendation/detail/"),
            ("recg.detik.com", "/article-recommendation/detail/"),
            ("recg.detik.com", "/article-recommendation/wp/"),
            ("recg.detik.com", "/article-recommendation/sticky/"),
            ("recg.detik.com", "/article-recommendation/index/"),
            # Authentication
            ("connect.detik.com", "/oauth/authorize"),
            ("connect.detik.com", "/accounts/register"),
            ("connect.detik.com", "/api/mpc/quickcard/html"),
            ("connect.detik.com", "/token/me.html"),
            # Comments
            ("apicomment.detik.com", "/detail-article/sneak-peek/"),
            # Tracking
            ("iat.detiknetwork.com", "/ip-information.js"),
            # Ad serving
            ("newrevive.detik.com", "/delivery/asyncjs.php"),
        ]

        # Test each pattern
        async with httpx.AsyncClient() as client:
            for api_domain, path in api_patterns:
                endpoint = f"https://{api_domain}{path}"

                # Quick test if endpoint is accessible
                try:
                    response = await client.head(
                        endpoint,
                        headers=self.headers,
                        timeout=5.0,
                        follow_redirects=True,
                    )

                    if response.status_code < 500:  # Any response except server error
                        self.detected_endpoints.add(endpoint)

                except Exception:
                    # Endpoint not accessible or timeout, skip
                    pass

        logger.info(
            f"    ✓ Verified {len([e for e in self.detected_endpoints if any(p[1] in e for p in api_patterns)])} known patterns"
        )

    def _is_api_endpoint(self, domain: str, path: str) -> bool:
        """
        Determine if a URL looks like an API endpoint.

        Args:
            domain: Domain name
            path: URL path

        Returns:
            bool: True if it looks like an API
        """
        # Check domain patterns
        api_domain_keywords = ["api", "rech", "recg", "connect", "analytic", "iat"]

        if any(keyword in domain.lower() for keyword in api_domain_keywords):
            return True

        # Check path patterns
        api_path_keywords = [
            "/api/",
            "/recommendation/",
            "/oauth/",
            "/delivery/",
            "/sneak-peek/",
        ]

        if any(keyword in path.lower() for keyword in api_path_keywords):
            return True

        # Check file extensions
        api_extensions = [".json", ".xml", ".js", ".php"]
        if any(path.endswith(ext) for ext in api_extensions):
            return True

        return False

    def categorize_endpoints(self) -> Dict[str, List[str]]:
        """
        Categorize detected endpoints by type.

        Returns:
            Dict with categorized endpoints
        """
        categories = {
            "recommendation": [],
            "authentication": [],
            "comment": [],
            "tracking": [],
            "ad_serving": [],
            "other": [],
        }

        for endpoint in self.detected_endpoints:
            categorized = False

            if "recommendation" in endpoint or "rech" in endpoint or "recg" in endpoint:
                categories["recommendation"].append(endpoint)
                categorized = True
            elif "oauth" in endpoint or "connect" in endpoint or "auth" in endpoint:
                categories["authentication"].append(endpoint)
                categorized = True
            elif "comment" in endpoint:
                categories["comment"].append(endpoint)
                categorized = True
            elif "analytic" in endpoint or "iat" in endpoint or "tracking" in endpoint:
                categories["tracking"].append(endpoint)
                categorized = True
            elif "revive" in endpoint or "delivery" in endpoint or "ad" in endpoint:
                categories["ad_serving"].append(endpoint)
                categorized = True

            if not categorized:
                categories["other"].append(endpoint)

        return categories


# Synchronous wrapper for testing
def detect_endpoints_sync(domain: str) -> Set[str]:
    """Synchronous wrapper for endpoint detection."""
    import asyncio

    detector = EndpointDetector()
    return asyncio.run(detector.detect(domain))
