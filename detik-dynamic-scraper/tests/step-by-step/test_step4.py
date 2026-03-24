"""Quick test for Content Scraper - Step 4."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.content_scraper import ContentScraper
import asyncio
import json


async def main():
    print("🧪 Quick Test - Content Scraper Engine")
    print("=" * 60)

    scraper = ContentScraper(rate_limit=0.5, max_retries=2)

    # Test 1: Scrape JSON API
    print("\n1️⃣ Test: Scrape from JSON API endpoint")
    print("  Fetching articles from recommendation API...\n")

    articles_json = await scraper.scrape(
        "https://recg.detik.com/article-recommendation/wp/test?size=10&nocache=1&ids=undefined&acctype=acc-detikcom",
        response_type="json",
    )

    print(f"  ✅ Scraped {len(articles_json)} articles from JSON API")
    if articles_json:
        print(f"     - Sample: {articles_json[0].get('title', 'N/A')[:60]}...")
        print(f"     - Has ID: {bool(articles_json[0].get('id'))}")
        print(f"     - Has URL: {bool(articles_json[0].get('url'))}")

    # Test 2: Scrape HTML page
    print("\n2️⃣ Test: Scrape from HTML page")
    print("  Fetching articles from news homepage...\n")

    articles_html = await scraper.scrape("https://news.detik.com", response_type="html")

    print(f"  ✅ Scraped {len(articles_html)} articles from HTML")
    if articles_html:
        print(f"     - Sample: {articles_html[0].get('title', 'N/A')[:60]}...")
        print(f"     - Has ID: {bool(articles_html[0].get('id'))}")
        print(f"     - Has URL: {bool(articles_html[0].get('url'))}")

    # Test 3: Ad filtering
    print("\n3️⃣ Test: Ad filtering")

    # Create fake articles with ads
    test_articles = [
        {"id": "1", "title": "Normal Article", "url": "https://news.detik.com/normal"},
        {"id": "2", "title": "Iklan Product", "url": "https://news.detik.com/iklan"},
        {
            "id": "3",
            "title": "Another Article",
            "url": "https://news.detik.com/article",
        },
        {"id": "4", "title": "Sponsored Content", "url": "https://ads.detik.com/promo"},
    ]

    filtered = scraper._filter_ads(test_articles)
    ads_removed = len(test_articles) - len(filtered)

    print(f"  ✅ Filtered {ads_removed} ads from {len(test_articles)} items")
    print(f"     - Remaining: {len(filtered)} legitimate articles")

    # Test 4: Deduplication
    print("\n4️⃣ Test: Deduplication")

    scraper.reset_deduplication()

    # Create duplicates
    duplicate_articles = [
        {"id": "A1", "title": "Article 1", "url": "https://news.detik.com/a1"},
        {"id": "A2", "title": "Article 2", "url": "https://news.detik.com/a2"},
        {
            "id": "A1",
            "title": "Article 1 Duplicate",
            "url": "https://news.detik.com/a1",
        },
        {"id": "A3", "title": "Article 3", "url": "https://news.detik.com/a3"},
        {
            "id": "A2",
            "title": "Article 2 Duplicate",
            "url": "https://news.detik.com/a2",
        },
    ]

    unique = scraper._deduplicate(duplicate_articles)
    duplicates_removed = len(duplicate_articles) - len(unique)

    print(
        f"  ✅ Removed {duplicates_removed} duplicates from {len(duplicate_articles)} items"
    )
    print(f"     - Unique: {len(unique)} articles")

    # Test 5: Data normalization
    print("\n5️⃣ Test: Data normalization")

    # Test with different JSON structures
    raw_article = {
        "id": "8412424",
        "title": "Test Article Title",
        "articleurl": "https://news.detik.com/test",
        "category": "news",
        "publish_date": "2026-03-23",
        "tags": "tag1,tag2,tag3",
    }

    normalized = scraper._normalize_article(raw_article, "https://api.detik.com/test")

    print(f"  ✅ Normalized article data:")
    print(f"     - ID: {normalized.get('id')}")
    print(
        f"     - Title: {normalized.get('title')[:40] if normalized.get('title') else 'N/A'}..."
    )
    print(f"     - Tags: {len(normalized.get('tags', []))} tags")
    print(f"     - Has timestamp: {bool(normalized.get('scraped_at'))}")

    print("\n" + "=" * 60)

    # Validation
    success_count = 0

    if len(articles_json) > 0:
        success_count += 1
    if len(articles_html) > 0:
        success_count += 1
    if ads_removed >= 2:
        success_count += 1
    if duplicates_removed >= 2:
        success_count += 1
    if normalized.get("id") and normalized.get("tags"):
        success_count += 1

    if success_count >= 4:
        print("✅ Step 4 tests PASSED!")
        print(f"   - {success_count}/5 test groups passed")
        print(f"   - JSON: {len(articles_json)} articles")
        print(f"   - HTML: {len(articles_html)} articles")
        print(f"   - Ads filtered: {ads_removed}")
        print(f"   - Duplicates removed: {duplicates_removed}")
        return True
    else:
        print("❌ Step 4 tests FAILED")
        print(f"   - Only {success_count}/5 test groups passed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
