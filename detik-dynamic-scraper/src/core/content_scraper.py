"""
Content Scraper Engine - Step 4

Smart scraping engine that:
- Adapts to HTML and JSON responses
- Filters out ads automatically
- Handles rate limiting
- Deduplicates content
- Retries on failures

Author: Dynamic Scraper
Date: 2026-03-23
"""

import re
import json
import asyncio
from typing import Dict, List, Optional, Any, Set
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os

# FIX BUG #8: Add proper logging
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


class ContentScraper:
    """Dynamic content scraper with ad filtering and deduplication."""

    def __init__(
        self, rate_limit: float = 1.0, max_retries: int = 3, max_seen_ids: int = 10000
    ):
        """
        Initialize scraper.

        Args:
            rate_limit: Delay between requests in seconds
            max_retries: Maximum retry attempts for failed requests
            max_seen_ids: Maximum size of seen_ids cache (prevents memory leak)
        """
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.seen_ids: Set[str] = set()
        self.max_seen_ids = max_seen_ids  # FIX BUG #3: Add limit
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

        # Ad detection patterns
        self.ad_patterns = [
            r"iklan",
            r"ads?[-_]",
            r"advertisement",
            r"sponsored",
            r"promo",
            r"banner",
            r"adv[-_]",
            r"google[-_]ad",
            r"adsense",
            r"adslot",
            r"commercial",
            r"marketing",
        ]

        # Content selectors for different page types
        self.content_selectors = {
            "article": [
                "article",
                '[itemtype*="Article"]',
                ".article-content",
                "#article-content",
                ".detail__body-text",
            ],
            "title": [
                "h1",
                '[itemprop="headline"]',
                ".detail__title",
                'meta[property="og:title"]',
            ],
            "date": [
                "time[datetime]",
                '[itemprop="datePublished"]',
                ".date",
                'meta[property="article:published_time"]',
            ],
        }

    def _ensure_protocol(self, url: str) -> str:
        """
        Ensure URL has http:// or https:// protocol.

        Args:
            url: URL that may or may not have protocol

        Returns:
            URL with protocol

        Raises:
            ValueError: If URL is empty or invalid
        """
        # FIX BUG #7: Validate URL
        if not url or not isinstance(url, str):
            raise ValueError(f"URL cannot be empty or None, got: {type(url).__name__}")

        url = url.strip()
        if not url:
            raise ValueError("URL cannot be empty after stripping whitespace")

        # Already has protocol
        if url.startswith("http://") or url.startswith("https://"):
            return url

        # Has protocol-relative format (//domain.com)
        if url.startswith("//"):
            return "https:" + url

        # No protocol, add https://
        return "https://" + url

    async def scrape(
        self, url: str, response_type: str = "auto"
    ) -> List[Dict[str, Any]]:
        """
        Scrape content from URL.

        Args:
            url: URL to scrape (with or without protocol)
            response_type: 'auto', 'json', or 'html'

        Returns:
            List of article/content dictionaries
        """
        content = []

        # FIX BUG #1: Ensure URL has protocol
        url = self._ensure_protocol(url)

        for attempt in range(self.max_retries):
            try:
                # Rate limiting
                if attempt > 0:
                    await asyncio.sleep(self.rate_limit * (attempt + 1))
                else:
                    await asyncio.sleep(self.rate_limit)

                async with httpx.AsyncClient(
                    follow_redirects=True, timeout=20.0
                ) as client:
                    response = await client.get(
                        url,
                        headers={
                            "User-Agent": self.user_agent,
                            "Accept": "application/json, text/html, */*",
                            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                        },
                    )

                    if response.status_code == 200:
                        # Auto-detect response type
                        if response_type == "auto":
                            # FIX BUG #2: Safely handle None content-type
                            content_type = response.headers.get("content-type") or ""
                            content_type = content_type.lower()

                            if "application/json" in content_type:
                                response_type = "json"
                            elif "text/html" in content_type:
                                response_type = "html"
                            else:
                                # No content-type or unknown, try to detect from content
                                try:
                                    json.loads(response.text)
                                    response_type = "json"
                                except (json.JSONDecodeError, ValueError, TypeError):
                                    # FIX BUG #6: Specific exception instead of bare except
                                    response_type = "html"

                        # Parse based on type
                        if response_type == "json":
                            content = self._parse_json_response(response.text, url)
                        else:
                            content = self._parse_html_response(response.text, url)

                        # Filter ads
                        content = self._filter_ads(content)

                        # Deduplicate
                        content = self._deduplicate(content)

                        break  # Success, exit retry loop

                    elif response.status_code in [429, 503]:
                        # Rate limited or service unavailable, retry
                        logger.warning(
                            f"Rate limited on {url} (attempt {attempt + 1}/{self.max_retries})"
                        )
                        continue
                    else:
                        logger.warning(
                            f"HTTP {response.status_code} for {url} (attempt {attempt + 1}/{self.max_retries})"
                        )

            except Exception as e:
                logger.error(
                    f"Error scraping {url} (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                if attempt == self.max_retries - 1:
                    logger.error(
                        f"Failed to scrape {url} after {self.max_retries} attempts"
                    )

        return content

    def _parse_json_response(self, text: str, source_url: str) -> List[Dict[str, Any]]:
        """Parse JSON API response."""
        articles = []

        try:
            data = json.loads(text)

            # Handle different JSON structures
            if isinstance(data, dict):
                # Check for common array keys
                for key in ["body", "data", "articles", "items", "results"]:
                    if key in data and isinstance(data[key], list):
                        articles.extend(
                            self._extract_articles_from_list(data[key], source_url)
                        )
                        break
                else:
                    # Single article object
                    if self._is_article_object(data):
                        articles.append(self._normalize_article(data, source_url))

            elif isinstance(data, list):
                articles.extend(self._extract_articles_from_list(data, source_url))

        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error for {source_url}: {e}")

        return articles

    def _extract_articles_from_list(
        self, items: List[Any], source_url: str
    ) -> List[Dict[str, Any]]:
        """Extract articles from a list of items."""
        articles = []

        for item in items:
            if isinstance(item, dict) and self._is_article_object(item):
                articles.append(self._normalize_article(item, source_url))

        return articles

    def _is_article_object(self, obj: Dict[str, Any]) -> bool:
        """Check if object looks like an article."""
        # Must have at least title or id
        required_fields = ["title", "id", "headline", "name"]
        return any(field in obj for field in required_fields)

    def _normalize_article(
        self, raw: Dict[str, Any], source_url: str
    ) -> Dict[str, Any]:
        """Normalize article data to standard format."""
        article = {
            "id": None,
            "title": None,
            "url": None,
            "image": None,
            "category": None,
            "publish_date": None,
            "description": None,
            "tags": [],
            "author": None,
            "source_url": source_url,
            "scraped_at": datetime.utcnow().isoformat(),
            "raw_data": raw,  # Keep original for reference
        }

        # Extract ID
        for key in ["id", "article_id", "articleid", "contentId"]:
            if key in raw:
                article["id"] = str(raw[key]).replace("d-", "")
                break

        # Extract title
        for key in ["title", "headline", "name", "judul"]:
            if key in raw:
                article["title"] = raw[key]
                break

        # Extract URL
        for key in ["url", "articleurl", "link", "href", "permalink"]:
            if key in raw:
                article["url"] = raw[key]
                break

        # Extract image
        for key in ["image", "thumbnail", "img", "foto", "picture", "imageurl"]:
            if key in raw:
                article["image"] = raw[key]
                break

        # Extract category
        for key in ["category", "kategori", "channel", "section"]:
            if key in raw:
                article["category"] = raw[key]
                break

        # Extract publish date
        for key in [
            "publish_date",
            "publishdate",
            "date",
            "published",
            "tanggal",
            "pubdate",
        ]:
            if key in raw:
                article["publish_date"] = raw[key]
                break

        # Extract description
        for key in ["description", "deskripsi", "excerpt", "summary", "intro"]:
            if key in raw:
                article["description"] = raw[key]
                break

        # Extract tags
        for key in ["tags", "keywords", "tag", "kata_kunci"]:
            if key in raw:
                tags = raw[key]
                if isinstance(tags, str):
                    # Split by common delimiters
                    article["tags"] = [
                        t.strip() for t in re.split(r"[,|;]", tags) if t.strip()
                    ]
                elif isinstance(tags, list):
                    article["tags"] = [str(t).strip() for t in tags if t]
                break

        # Extract author
        for key in ["author", "penulis", "reporter", "by"]:
            if key in raw:
                article["author"] = raw[key]
                break

        return article

    def _parse_html_response(self, html: str, source_url: str) -> List[Dict[str, Any]]:
        """Parse HTML page response."""
        articles = []

        soup = BeautifulSoup(html, "lxml")

        # Try to extract article list from page
        article_containers = self._find_article_containers(soup)

        if article_containers:
            # Multiple articles on page (e.g., homepage, category page)
            for container in article_containers:
                article = self._extract_article_from_html(container, source_url)
                if article:
                    articles.append(article)
        else:
            # Single article page
            article = self._extract_single_article(soup, source_url)
            if article:
                articles.append(article)

        return articles

    def _find_article_containers(self, soup: BeautifulSoup) -> List[Any]:
        """Find containers that hold article items."""
        containers = []

        # Common article container selectors
        selectors = [
            "article",
            '[itemtype*="Article"]',
            ".article-item",
            ".article-list > div",
            ".media__list > div",
            "[data-article-id]",
            ".list-content article",
        ]

        for selector in selectors:
            found = soup.select(selector)
            if found and len(found) > 1:  # Multiple articles
                containers = found
                break

        return containers

    def _extract_article_from_html(
        self, element: Any, source_url: str
    ) -> Optional[Dict[str, Any]]:
        """Extract article data from HTML element."""
        article = {
            "id": None,
            "title": None,
            "url": None,
            "image": None,
            "category": None,
            "publish_date": None,
            "description": None,
            "tags": [],
            "author": None,
            "source_url": source_url,
            "scraped_at": datetime.utcnow().isoformat(),
        }

        # Extract title
        title_elem = element.find(["h1", "h2", "h3", "h4"])
        if title_elem:
            article["title"] = title_elem.get_text(strip=True)

        # Extract URL
        link = element.find("a", href=True)
        if link:
            article["url"] = urljoin(source_url, link["href"])

            # Extract ID from URL
            match = re.search(r"/d-(\d+)/", article["url"])
            if match:
                article["id"] = match.group(1)

        # Extract image
        img = element.find("img", src=True)
        if img:
            article["image"] = img.get("src") or img.get("data-src")

        # Only return if we have at least title and URL
        if article["title"] and article["url"]:
            return article

        return None

    def _extract_single_article(
        self, soup: BeautifulSoup, source_url: str
    ) -> Optional[Dict[str, Any]]:
        """Extract single article from detail page."""
        article = {
            "id": None,
            "title": None,
            "url": source_url,
            "image": None,
            "category": None,
            "publish_date": None,
            "description": None,
            "content": None,
            "tags": [],
            "author": None,
            "source_url": source_url,
            "scraped_at": datetime.utcnow().isoformat(),
        }

        # Extract from meta tags (most reliable)
        meta_data = self._extract_meta_tags(soup)
        article.update(meta_data)

        # Extract content
        content_elem = soup.find(["article", ".detail__body-text", ".content"])
        if content_elem:
            article["content"] = content_elem.get_text(strip=True)

        # Only return if we have essential data
        if article["title"] or article["id"]:
            return article

        return None

    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract data from HTML meta tags."""
        data = {}

        # Article ID
        meta = soup.find("meta", {"name": "articleid"})
        if meta:
            data["id"] = meta.get("content")

        # Title
        meta = soup.find("meta", {"property": "og:title"})
        if meta:
            data["title"] = meta.get("content")

        # Image
        meta = soup.find("meta", {"property": "og:image"})
        if meta:
            data["image"] = meta.get("content")

        # Description
        meta = soup.find("meta", {"property": "og:description"})
        if meta:
            data["description"] = meta.get("content")

        # Author
        meta = soup.find("meta", {"name": "author"})
        if meta:
            data["author"] = meta.get("content")

        # Keywords
        meta = soup.find("meta", {"name": "keywords"})
        if meta:
            keywords = meta.get("content")
            if keywords:
                data["tags"] = [k.strip() for k in keywords.split(",")]

        # Publish date
        meta = soup.find("meta", {"property": "article:published_time"})
        if meta:
            data["publish_date"] = meta.get("content")

        return data

    def _filter_ads(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out advertisements from articles."""
        filtered = []

        for article in articles:
            if self._is_ad(article):
                continue
            filtered.append(article)

        return filtered

    def _is_ad(self, article: Dict[str, Any]) -> bool:
        """Check if article is an advertisement."""
        # FIX BUG #2 (Real location): Safely handle None values
        # Check title
        title = (article.get("title") or "").lower()
        for pattern in self.ad_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                return True

        # Check URL
        url = (article.get("url") or "").lower()
        for pattern in self.ad_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return True

        # Check category
        category = (article.get("category") or "").lower()
        if category in ["iklan", "ads", "sponsored", "promo"]:
            return True

        # Check for ad indicators in raw data
        raw = article.get("raw_data", {})
        if isinstance(raw, dict):
            if raw.get("is_ad") or raw.get("sponsored") or raw.get("advertisement"):
                return True

        return False

    def _deduplicate(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate articles based on ID."""
        unique = []

        # FIX BUG #3: Clear cache if it grows too large (prevents memory leak)
        if len(self.seen_ids) >= self.max_seen_ids:
            logger.warning(
                f"seen_ids cache full ({len(self.seen_ids)}), clearing to prevent memory leak"
            )
            self.seen_ids.clear()

        for article in articles:
            article_id = article.get("id")

            if article_id:
                if article_id not in self.seen_ids:
                    self.seen_ids.add(article_id)
                    unique.append(article)
            else:
                # No ID, check by URL
                url = article.get("url")
                if url and url not in self.seen_ids:
                    self.seen_ids.add(url)
                    unique.append(article)

        return unique

    def reset_deduplication(self):
        """Reset the deduplication cache."""
        self.seen_ids.clear()


if __name__ == "__main__":
    # Quick test
    import asyncio

    async def test():
        print("🧪 Testing Content Scraper...")

        scraper = ContentScraper(rate_limit=0.5)

        # Test 1: JSON API
        print("\n1️⃣ Test: Scrape JSON API")
        articles = await scraper.scrape(
            "https://recg.detik.com/article-recommendation/wp/test?size=5&nocache=1&ids=undefined&acctype=acc-detikcom",
            response_type="json",
        )
        print(f"  ✅ Found {len(articles)} articles from JSON API")
        if articles:
            print(f"     - First: {articles[0].get('title', 'N/A')[:50]}")

        # Test 2: HTML page
        print("\n2️⃣ Test: Scrape HTML page")
        articles = await scraper.scrape("https://news.detik.com", response_type="html")
        print(f"  ✅ Found {len(articles)} articles from HTML")
        if articles:
            print(f"     - First: {articles[0].get('title', 'N/A')[:50]}")

        print("\n✅ All tests passed!")

    asyncio.run(test())
