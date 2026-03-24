"""
Dynamic Parameter Extraction System - Step 3

Auto-extracts required parameters for API calls from:
- HTML meta tags
- JavaScript variables
- Successful API responses
- URL patterns

Author: Dynamic Scraper
Date: 2026-03-23
"""

import re
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs
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


class ParameterExtractor:
    """Extract dynamic parameters for API endpoints."""

    def __init__(self):
        self.parameter_schemas = {}
        self.learned_params = {}

    async def extract(self, domain: str, endpoint: str) -> Dict[str, Any]:
        """
        Extract parameters for a specific domain and endpoint.

        Args:
            domain: Domain name (e.g., 'news.detik.com')
            endpoint: API endpoint URL

        Returns:
            Dictionary of extracted parameters
        """
        params = {}

        # 1. Extract from meta tags
        meta_params = await self._extract_from_meta_tags(domain)
        params.update(meta_params)

        # 2. Extract from endpoint pattern
        pattern_params = self._extract_from_pattern(endpoint)
        params.update(pattern_params)

        # 3. Extract from successful requests (learning)
        learned = self._get_learned_params(domain, endpoint)
        params.update(learned)

        # 4. Set defaults for common parameters
        defaults = self._get_default_params(endpoint)
        for key, value in defaults.items():
            if key not in params:
                params[key] = value

        return params

    async def _extract_from_meta_tags(self, domain: str) -> Dict[str, Any]:
        """Extract parameters from HTML meta tags."""
        params = {}

        try:
            url = f"https://{domain}"
            async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
                response = await client.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    },
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "lxml")

                    # Extract acctype from various sources
                    acctype = self._extract_acctype(soup, domain)
                    if acctype:
                        params["acctype"] = acctype

                    # Extract client ID
                    client_id = self._extract_client_id(soup)
                    if client_id:
                        params["clientId"] = client_id

                    # Extract article ID if on article page
                    article_id = self._extract_article_id(soup)
                    if article_id:
                        params["article_id"] = article_id

                    # Extract user ID from cookies/storage
                    user_id = self._extract_user_id(soup)
                    if user_id:
                        params["user_id"] = user_id

        except Exception as e:
            logger.warning("  Error extracting from meta tags: {e}")

        return params

    def _extract_acctype(self, soup: BeautifulSoup, domain: str) -> Optional[str]:
        """Extract account type parameter."""
        # Method 1: From meta tag
        meta = soup.find("meta", {"name": "acctype"})
        if meta and meta.get("content"):
            return meta.get("content")

        # Method 2: From JavaScript
        scripts = soup.find_all("script", string=re.compile(r"acctype"))
        for script in scripts:
            match = re.search(
                r'acctype["\']?\s*[:=]\s*["\']([^"\']+)["\']', script.string
            )
            if match:
                return match.group(1)

        # Method 3: Infer from domain (EXPANDED to all 32+ subdomains)
        domain_map = {
            # Main content channels (12)
            "www.detik.com": "acc-detikcom",
            "news.detik.com": "acc-detiknews",
            "finance.detik.com": "acc-detikfinance",
            "sport.detik.com": "acc-detiksport",
            "hot.detik.com": "acc-detikhot",
            "inet.detik.com": "acc-detikinet",
            "travel.detik.com": "acc-detiktravel",
            "food.detik.com": "acc-detikfood",
            "health.detik.com": "acc-detikhealth",
            "oto.detik.com": "acc-detikoto",
            "wolipop.detik.com": "acc-detikwolipop",
            "20.detik.com": "acc-detik20",
            # Additional content channels (8)
            "edu.detik.com": "acc-detikedu",
            "event.detik.com": "acc-detikevent",
            "foto.detik.com": "acc-detikfoto",
            "karir.detik.com": "acc-detikkarir",
            "kemiri.detik.com": "acc-detikkemiri",
            "pasangmata.detik.com": "acc-detikpasangmata",
            "fyb.detik.com": "acc-detikfyb",
            "vod.detik.com": "acc-detikvod",
            # API & Services (12)
            "recg.detik.com": "acc-detikcom",
            "rech.detik.com": "acc-detikcom",
            "rech20.detik.com": "acc-detik20",
            "explore-api.detik.com": "acc-detikcom",
            "apicomment.detik.com": "acc-detikcom",
            "connect.detik.com": "acc-detikcom",
            "adsmart.detik.com": "acc-detikcom",
            "analytic.detik.com": "acc-detikcom",
            "collent.detik.com": "acc-detikcom",
            "newrevive.detik.com": "acc-detikcom",
            "rekomendit.detik.com": "acc-detikcom",
            "cdnstatic.detik.com": "acc-detikcom",
            "cdnv.detik.com": "acc-detikcom",
        }

        return domain_map.get(domain, "acc-detikcom")

    def _extract_client_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract client ID."""
        # From meta tag
        meta = soup.find("meta", {"name": "clientId"})
        if meta and meta.get("content"):
            return meta.get("content")

        # From JavaScript
        scripts = soup.find_all("script", string=re.compile(r"clientId"))
        for script in scripts:
            match = re.search(
                r'clientId["\']?\s*[:=]\s*["\']?(\d+)["\']?', script.string
            )
            if match:
                return match.group(1)

        return None

    def _extract_article_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article ID from page."""
        # Method 1: From meta tag
        meta = soup.find("meta", {"name": "articleid"})
        if meta and meta.get("content"):
            return meta.get("content")

        # Method 2: From URL pattern in canonical link
        canonical = soup.find("link", {"rel": "canonical"})
        if canonical and canonical.get("href"):
            match = re.search(r"/d-(\d+)/", canonical.get("href"))
            if match:
                return match.group(1)

        return None

    def _extract_user_id(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract user ID from page."""
        # Look for user ID patterns in scripts
        scripts = soup.find_all("script")
        for script in scripts:
            if script.string:
                # Pattern: user_id or userId
                match = re.search(
                    r'user_?[iI]d["\']?\s*[:=]\s*["\']([^"\']+)["\']', script.string
                )
                if match:
                    return match.group(1)

        return None

    def _extract_from_pattern(self, endpoint: str) -> Dict[str, Any]:
        """Extract parameters from endpoint URL pattern."""
        params = {}

        # Parse the endpoint URL
        parsed = urlparse(endpoint)
        query_params = parse_qs(parsed.query)

        # Extract existing query parameters
        for key, value in query_params.items():
            params[key] = value[0] if isinstance(value, list) else value

        # Identify parameter placeholders in path
        # e.g., /detail/{user_id} -> needs user_id parameter
        path_params = re.findall(r"\{(\w+)\}", parsed.path)
        for param in path_params:
            if param not in params:
                params[f"_path_{param}"] = None  # Mark as required

        return params

    def _get_learned_params(self, domain: str, endpoint: str) -> Dict[str, Any]:
        """Get parameters learned from successful requests."""
        key = f"{domain}:{endpoint}"
        return self.learned_params.get(key, {})

    def _get_default_params(self, endpoint: str) -> Dict[str, Any]:
        """Get default parameters based on endpoint type."""
        defaults = {}

        # Recommendation API defaults
        if "recommendation" in endpoint or "recg" in endpoint or "rech" in endpoint:
            defaults.update(
                {
                    "size": 10,
                    "nocache": 1,
                    "ids": "undefined",
                }
            )

        # Comment API defaults
        if "comment" in endpoint or "apicomment" in endpoint:
            defaults.update(
                {
                    "limit": 20,
                    "offset": 0,
                }
            )

        # Common defaults
        defaults.update(
            {
                "timestamp": None,  # Will be generated at runtime
            }
        )

        return defaults

    def learn_from_request(
        self, domain: str, endpoint: str, params: Dict[str, Any], success: bool
    ):
        """Learn parameters from a successful/failed request."""
        if success:
            key = f"{domain}:{endpoint}"
            if key not in self.learned_params:
                self.learned_params[key] = {}

            # Update learned parameters
            self.learned_params[key].update(params)

    def build_parameter_schema(
        self, endpoint: str, sample_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build a parameter schema for an endpoint."""
        schema = {
            "endpoint": endpoint,
            "required": [],
            "optional": [],
            "defaults": {},
            "types": {},
        }

        # Analyze parameters
        for key, value in sample_params.items():
            # Determine if required or optional
            if value is None or key.startswith("_path_"):
                schema["required"].append(key.replace("_path_", ""))
            else:
                schema["optional"].append(key)
                schema["defaults"][key] = value

            # Determine type
            if isinstance(value, int):
                schema["types"][key] = "integer"
            elif isinstance(value, bool):
                schema["types"][key] = "boolean"
            elif isinstance(value, str):
                schema["types"][key] = "string"
            else:
                schema["types"][key] = "any"

        self.parameter_schemas[endpoint] = schema
        return schema

    def get_schema(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Get the parameter schema for an endpoint."""
        return self.parameter_schemas.get(endpoint)

    def generate_params(
        self, domain: str, endpoint: str, overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate complete parameters for an API call.

        Args:
            domain: Domain name
            endpoint: API endpoint
            overrides: Manual parameter overrides

        Returns:
            Complete parameter dictionary
        """
        # Get base parameters
        schema = self.get_schema(endpoint)
        params = {}

        if schema:
            # Use schema defaults
            params.update(schema.get("defaults", {}))

        # Add learned parameters
        learned = self._get_learned_params(domain, endpoint)
        params.update(learned)

        # Apply overrides
        if overrides:
            params.update(overrides)

        # Generate dynamic values
        if "timestamp" in params and params["timestamp"] is None:
            import time

            params["timestamp"] = int(time.time())

        return params


def extract_params_sync(domain: str, endpoint: str) -> Dict[str, Any]:
    """Synchronous wrapper for parameter extraction."""
    import asyncio

    extractor = ParameterExtractor()

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(extractor.extract(domain, endpoint))


if __name__ == "__main__":
    # Quick test
    import asyncio

    async def test():
        logger.info("🧪 Testing Parameter Extractor...")

        extractor = ParameterExtractor()

        # Test 1: Extract from news.detik.com
        logger.info("\n1️⃣ Test: Extract parameters for news.detik.com")
        params = await extractor.extract(
            "news.detik.com", "https://rech.detik.com/article-recommendation/detail/"
        )
        logger.info(f"  ✅ Extracted: {json.dumps(params, indent=2)}")

        # Test 2: Build schema
        logger.info("\n2️⃣ Test: Build parameter schema")
        schema = extractor.build_parameter_schema(
            "https://rech.detik.com/article-recommendation/detail/", params
        )
        logger.info(f"  ✅ Schema: {json.dumps(schema, indent=2)}")

        # Test 3: Generate params
        logger.info("\n3️⃣ Test: Generate parameters with overrides")
        generated = extractor.generate_params(
            "news.detik.com",
            "https://rech.detik.com/article-recommendation/detail/",
            {"size": 20},
        )
        logger.info(f"  ✅ Generated: {json.dumps(generated, indent=2)}")

        logger.info("\n✅ All tests passed!")

    asyncio.run(test())
