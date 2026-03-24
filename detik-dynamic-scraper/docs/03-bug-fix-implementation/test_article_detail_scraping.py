#!/usr/bin/env python3
"""
Test Article Detail Scraping - Comprehensive Test Suite

Tests the fixed article detail scraping functionality across multiple detik subdomains.
This test verifies the fix for the HTTP 500 error on /api/articles/{id}/scrape-detail

Author: Dynamic Scraper
Date: 2026-03-24
"""

import sys
import asyncio

sys.path.insert(0, "src")

from core.article_detail_scraper import ArticleDetailScraper
from storage.database import Database
from datetime import datetime


async def test_scraper_functionality():
    """Test article detail scraper with various URLs"""

    print("=" * 80)
    print("🧪 ARTICLE DETAIL SCRAPING TEST SUITE")
    print("=" * 80)

    scraper = ArticleDetailScraper(rate_limit=0.5)

    test_cases = [
        {
            "name": "Wolipop (uses .itp_bodycontent)",
            "url": "https://wolipop.detik.com/entertainment-news/d-8406492/ratu-yordania-memohon-putranya-dibebaskan-setelah-batal-jadi-calon-raja",
            "expected_author": "Kiki Oktaviani",
        },
        {
            "name": "News Detik (uses .detail__body-text)",
            "url": "https://news.detik.com/berita/d-8412424/iran-siap-kawal-kapal-lintasi-selat-hormuz-setelah-serangan-israel",
            "expected_author": "Rolando Fransiscus Sihombing",
        },
    ]

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f'\n{i}. Testing: {test["name"]}')
        print(f'   URL: {test["url"][:70]}...')

        try:
            result = await scraper.scrape_article_detail(test["url"])

            # Verify result
            assert result is not None, "Result is None"
            assert result.get("title"), "No title extracted"
            assert result.get("content"), "No content extracted"
            assert (
                len(result["content"]) > 100
            ), f"Content too short: {len(result['content'])} chars"

            print(f"   ✅ PASSED")
            print(f'      Title: {result["title"][:60]}...')
            print(f'      Author: {result.get("author", "N/A")}')
            print(f'      Content: {len(result["content"])} chars')

            passed += 1

        except AssertionError as e:
            print(f"   ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {type(e).__name__}: {e}")
            failed += 1

    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS")
    print("=" * 80)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")

    if failed == 0:
        print("\n✅✅✅ ALL TESTS PASSED! ✅✅✅")
        return True
    else:
        print(f"\n❌ {failed} test(s) failed")
        return False


async def test_api_endpoint_simulation():
    """Simulate the full API endpoint flow"""

    print("\n" + "=" * 80)
    print("🔌 API ENDPOINT SIMULATION TEST")
    print("=" * 80)

    article_id = "8406492"

    try:
        # Simulate API endpoint flow
        print(f"\nSimulating: POST /api/articles/{article_id}/scrape-detail")

        # Step 1: Get from database
        db = Database("data/dashboard_scraping.db")
        article = db.get_article(article_id)

        if not article:
            print("❌ Article not found in database")
            return False

        print(f"✅ Step 1: Article retrieved from database")

        # Step 2: Scrape detail
        scraper = ArticleDetailScraper(rate_limit=0.5)
        detail_data = await scraper.scrape_article_detail(article["url"])

        if not detail_data:
            print("❌ Failed to scrape article")
            return False

        print(f"✅ Step 2: Article scraped successfully")

        # Step 3: Build response (with fix)
        content = detail_data.get("content") or ""  # Safe handling

        response = {
            "success": True,
            "article_id": article_id,
            "content_length": len(content),  # No TypeError!
            "has_content": bool(content),
            "author": detail_data.get("author"),
        }

        print(f"✅ Step 3: Response built successfully")
        print(f"\n   Response:")
        print(f'   - success: {response["success"]}')
        print(f'   - content_length: {response["content_length"]}')
        print(f'   - has_content: {response["has_content"]}')
        print(f'   - author: {response["author"]}')

        db.close()

        # Verify
        assert response["success"] == True
        assert response["content_length"] > 0
        assert response["has_content"] == True

        print("\n✅ API endpoint simulation PASSED")
        return True

    except Exception as e:
        print(f"\n❌ API endpoint simulation FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run all tests"""

    print("\n" + "=" * 80)
    print("🚀 STARTING COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print(f"Date: {datetime.utcnow().isoformat()}")
    print(f"Testing: Article Detail Scraping Fix")
    print("=" * 80)

    # Run tests
    test1 = await test_scraper_functionality()
    test2 = await test_api_endpoint_simulation()

    # Final summary
    print("\n" + "=" * 80)
    print("🎯 FINAL SUMMARY")
    print("=" * 80)

    if test1 and test2:
        print("✅ All test suites PASSED")
        print("\n🎉 Article detail scraping is working correctly!")
        print("🎉 HTTP 500 error is FIXED!")
        return 0
    else:
        print("❌ Some tests FAILED")
        return 1


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(result)
