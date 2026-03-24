"""
Article Detail Scraper - Extract Full Article Content

Scrapes individual article pages to get:
- Full article content (body text)
- Author details
- Related articles
- Publish date
- Comments (optional)

Author: Dynamic Scraper
Date: 2026-03-24
"""

import re
import asyncio
from typing import Dict, Optional, Any
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


class ArticleDetailScraper:
    """Scrape full content from article detail pages."""

    def __init__(self, rate_limit: float = 1.0):
        """
        Initialize article detail scraper.

        Args:
            rate_limit: Delay between requests
        """
        self.rate_limit = rate_limit
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"

    async def scrape_article_detail(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape full article content from detail page.

        Args:
            url: Article detail page URL

        Returns:
            Dictionary with full article data
        """
        # Rate limiting
        await asyncio.sleep(self.rate_limit)

        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
                response = await client.get(
                    url, headers={"User-Agent": self.user_agent}
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "lxml")

                    # Extract all images and videos
                    all_images = self._extract_all_images(soup)
                    all_videos = self._extract_videos(soup)

                    # Extract article data
                    article = {
                        "url": url,
                        "title": self._extract_title(soup),
                        "content": self._extract_content(soup),
                        "author": self._extract_author(soup),
                        "publish_date": self._extract_publish_date(soup),
                        "category": self._extract_category(soup),
                        "tags": self._extract_tags(soup),
                        "image": self._extract_image(soup),
                        "related_articles": self._extract_related_articles(soup),
                        # New: Media metadata
                        "images": all_images,
                        "videos": all_videos,
                        "has_media": len(all_images) > 0 or len(all_videos) > 0,
                    }

                    return article
                else:
                    logger.warning(f"  HTTP {response.status_code} for {url}")
                    return None

        except Exception as e:
            logger.warning(f"  Error scraping {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article title."""
        # Try meta tag first
        meta = soup.find("meta", {"property": "og:title"})
        if meta and meta.get("content"):
            return meta.get("content")

        # Try h1
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        # Try title tag
        title = soup.find("title")
        if title:
            return title.get_text(strip=True)

        return None

    def _extract_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract full article content (main body text)."""
        # Try common article content selectors
        selectors = [
            ".itp_bodycontent",  # Wolipop, detikfood, and other detik subdomains
            ".detail__body-text",  # News, finance, etc.
            ".detail__body",  # General detik article body
            ".detail__body-detail",  # Some specific sections
            ".detail__text",  # Photo descriptions in some layouts
            "article .detail__body-text",
            '[itemprop="articleBody"]',
            ".article-content",
            "#article-content",
            ".entry-content",
            "article",  # Fallback to article tag
        ]

        for selector in selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Get all paragraph text
                paragraphs = content_elem.find_all(
                    ["p", "h2", "h3", "div.detail__body-text", "div.itp_bodycontent"]
                )
                if paragraphs:
                    # Join all paragraphs
                    content = "\n\n".join(
                        [
                            p.get_text(strip=True)
                            for p in paragraphs
                            if p.get_text(strip=True)
                            and len(p.get_text(strip=True))
                            > 10  # Lowered limit for photo/video descriptions
                        ]
                    )

                    if len(content) > 50:  # Lowered limit to catch short descriptions
                        return content

        # Fallback 1: Try meta description if body is empty (common for video-only pages)
        meta_desc = soup.find("meta", {"property": "og:description"}) or soup.find(
            "meta", {"name": "description"}
        )
        if meta_desc and meta_desc.get("content"):
            desc = meta_desc.get("content")
            if len(desc) > 50:
                return desc

        # Fallback 2: Just return first paragraph if found anywhere
        p = soup.find("p")
        if p and len(p.get_text(strip=True)) > 50:
            return p.get_text(strip=True)

        return None

    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article author."""
        # Try meta tag
        meta = soup.find("meta", {"name": "author"})
        if meta and meta.get("content"):
            return meta.get("content")

        # Try common author selectors
        selectors = [".detail__author", ".author-name", '[itemprop="author"]']
        for selector in selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                return author_elem.get_text(strip=True)

        return None

    def _extract_publish_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract publish date."""
        # Try meta tag
        meta = soup.find("meta", {"property": "article:published_time"})
        if meta and meta.get("content"):
            return meta.get("content")

        # Try time tag
        time_elem = soup.find("time", {"datetime": True})
        if time_elem:
            return time_elem.get("datetime")

        return None

    def _extract_category(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article category."""
        # Try breadcrumb
        breadcrumb = soup.select_one(".breadcrumb")
        if breadcrumb:
            links = breadcrumb.find_all("a")
            if len(links) > 1:
                return links[-1].get_text(strip=True)

        return None

    def _extract_tags(self, soup: BeautifulSoup) -> list:
        """Extract article tags."""
        tags = []

        # Try meta keywords
        meta = soup.find("meta", {"name": "keywords"})
        if meta and meta.get("content"):
            keywords = meta.get("content")
            tags = [k.strip() for k in keywords.split(",") if k.strip()]

        # Try tag elements
        tag_container = soup.select_one(".tag-list, .article-tags")
        if tag_container:
            tag_links = tag_container.find_all("a")
            tags.extend([a.get_text(strip=True) for a in tag_links])

        return list(set(tags))[:10]  # Limit to 10 unique tags

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main article image."""
        # Try og:image
        meta = soup.find("meta", {"property": "og:image"})
        if meta and meta.get("content"):
            return meta.get("content")

        # Try first image in article
        article = soup.find("article")
        if article:
            img = article.find("img", src=True)
            if img:
                return img.get("src")

        return None

    def _extract_all_images(self, soup: BeautifulSoup) -> list:
        """
        Extract all images from article (main + body images).

        Returns:
            List of dicts with image data: [{'url': str, 'alt': str, 'type': str, 'position': int}]
        """
        images = []

        # 1. Main image from og:image
        og_image = soup.find("meta", {"property": "og:image"})
        if og_image and og_image.get("content"):
            images.append(
                {
                    "url": og_image.get("content"),
                    "alt": "Main image",
                    "type": "main",
                    "position": 0,
                }
            )

        # 2. Body images from article content
        # Try multiple selectors for different detik domains
        selectors = [
            ".itp_bodycontent",  # wolipop, detikfood
            ".detail__body-text",  # news, travel, health
            ".detail__body",  # general
            "article",  # fallback
        ]

        for selector in selectors:
            article_body = soup.select_one(selector)
            if article_body:
                imgs = article_body.find_all("img", src=True)
                position = 1

                for img in imgs:
                    src = img.get("src", "")
                    alt = img.get("alt", "")

                    # Filter out non-content images
                    if self._is_valid_content_image(src):
                        images.append(
                            {
                                "url": src,
                                "alt": alt,
                                "type": "body",
                                "position": position,
                            }
                        )
                        position += 1

                # Found images, stop looking
                if position > 1:
                    break

        return images

    def _is_valid_content_image(self, url: str) -> bool:
        """
        Check if image URL is valid content image (not placeholder/logo).

        Args:
            url: Image URL to validate

        Returns:
            True if valid content image
        """
        # Filter out common non-content images
        exclude_patterns = [
            "loading.gif",
            "placeholder",
            "logo",
            "icon",
            "avatar",
            "ads",
            "advertisement",
            "tracking",
            "pixel.gif",
            "1x1.gif",
        ]

        url_lower = url.lower()

        # Check if URL contains any exclude pattern
        for pattern in exclude_patterns:
            if pattern in url_lower:
                return False

        # Must be from detik CDN or valid image domain
        valid_domains = [
            "awsimages.detik.net.id",
            "cdnstatic.detik.com",
            "detik.com",
        ]

        # Check if from valid domain
        for domain in valid_domains:
            if domain in url_lower:
                return True

        return False

    def _extract_videos(self, soup: BeautifulSoup) -> list:
        """
        Extract video embeds from article.

        Returns:
            List of dicts with video data: [{'url': str, 'title': str, 'platform': str, 'embed_code': str}]
        """
        videos = []
        seen_urls = set()  # Avoid duplicates

        # 1. NEW: Check meta tag video_story_url (Very common in detiktv layouts)
        meta_video = soup.find("meta", {"name": "video_story_url"}) or soup.find("meta", {"name": "dtk:video_story_url"})
        if meta_video and meta_video.get("content"):
            url = meta_video.get("content")
            if url not in seen_urls:
                seen_urls.add(url)
                videos.append({
                    "url": url,
                    "title": self._extract_title(soup) or "Video",
                    "platform": "20detik",
                    "embed_code": ""
                })

        # 2. Find 20.detik.com video links
        video_links = soup.find_all("a", href=lambda x: x and "20.detik.com" in x)

        for link in video_links:
            href = link.get("href", "")
            text = link.get_text(strip=True)

            # Check if it's a video link
            if (
                "/embed/" in href
                or "gambas:video" in text.lower()
                or "video" in href.lower()
            ):
                # Avoid duplicates
                if href in seen_urls:
                    continue
                seen_urls.add(href)

                # Try to find video title
                title = None

                # Look for "Video: ..." pattern in nearby text
                parent = link.parent
                if parent:
                    # Check parent text
                    parent_text = parent.get_text(strip=True)
                    if "Video:" in parent_text:
                        # Extract title after "Video:"
                        match = re.search(r"Video:\s*(.+?)(?:\[|$)", parent_text)
                        if match:
                            title = match.group(1).strip()

                # Fallback to link text
                if not title:
                    title = text if text and len(text) > 5 else "Video"

                videos.append(
                    {
                        "url": href,
                        "title": title,
                        "platform": "20detik",
                        "embed_code": text,
                    }
                )

        # 2. Find iframe embeds (additional videos)
        iframes = soup.find_all("iframe", src=True)
        for iframe in iframes:
            src = iframe.get("src", "")

            # Check if it's a video iframe (20.detik.com or youtube)
            if "20.detik.com" in src or "youtube.com" in src or "youtu.be" in src:
                if src in seen_urls:
                    continue
                seen_urls.add(src)

                # Determine platform
                if "20.detik.com" in src:
                    platform = "20detik"
                elif "youtube" in src or "youtu.be" in src:
                    platform = "youtube"
                else:
                    platform = "other"

                # Try to get title from iframe attributes or nearby text
                title = iframe.get("title", "Video")

                videos.append(
                    {"url": src, "title": title, "platform": platform, "embed_code": ""}
                )

        return videos

    def _extract_related_articles(self, soup: BeautifulSoup) -> list:
        """Extract related articles."""
        related = []

        # Try common related article containers
        selectors = [".related-articles a", ".widget-related a", ".artikel-terkait a"]

        for selector in selectors:
            links = soup.select(selector)
            for link in links[:5]:  # Max 5 related
                title = link.get_text(strip=True)
                href = link.get("href")
                if title and href and len(title) > 10:
                    related.append({"title": title, "url": href})

            if related:
                break

        return related


if __name__ == "__main__":
    # Quick test
    import asyncio

    async def test():
        logger.info("🧪 Testing Article Detail Scraper...")

        scraper = ArticleDetailScraper(rate_limit=0.5)

        # Test with sample URL
        test_url = "https://news.detik.com/berita/d-8412424/iran-siap-kawal-kapal-lintasi-selat-hormuz-setelah-serangan-israel"

        logger.info(f"\nScraping: {test_url[:60]}...")

        article = await scraper.scrape_article_detail(test_url)

        if article:
            logger.info("\n✅ Article scraped successfully!")
            logger.info(f"\nTitle: {article.get('title', 'N/A')[:80]}")
            logger.info(f"Author: {article.get('author', 'N/A')}")
            logger.info(f"Date: {article.get('publish_date', 'N/A')}")
            logger.info(f"Category: {article.get('category', 'N/A')}")
            logger.info(f"Tags: {len(article.get('tags', []))} tags")
            logger.info(f"Related: {len(article.get('related_articles', []))} articles")

            content = article.get("content", "")
            if content:
                logger.info(f"\n✅ Content extracted: {len(content)} characters")
                logger.info(f"Preview: {content[:200]}...")
            else:
                logger.info("\n❌ No content extracted")
        else:
            logger.info("\n❌ Failed to scrape article")

    asyncio.run(test())
