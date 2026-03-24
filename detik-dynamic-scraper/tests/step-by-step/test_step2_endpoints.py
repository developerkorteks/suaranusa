"""Test Step 2: Endpoint Detection Integration."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from core.comprehensive_scraper import ComprehensiveScraper


async def main():
    print("🧪 TEST STEP 2: Endpoint Detection Integration")
    print("=" * 70)

    scraper = ComprehensiveScraper(rate_limit=0.5, max_workers=3)

    # Test 1: Detect endpoints
    print("\n1️⃣ Test: Endpoint Detection")
    endpoints = await scraper._detect_endpoints("news.detik.com")

    print(f"\n✅ Detected {len(endpoints)} endpoints")

    # Filter recommendation endpoints
    recommendation = [ep for ep in endpoints if "article-recommendation" in str(ep)]
    print(f"✅ Recommendation endpoints: {len(recommendation)}")
    for i, ep in enumerate(sorted(recommendation), 1):
        print(f"  {i}. {ep}")

    # Test 2: Test API scraping with detected endpoints
    print("\n2️⃣ Test: Scrape using detected endpoints")

    articles = await scraper._scrape_api_endpoints("news.detik.com", 10)
    print(f"\n✅ Scraped {len(articles)} articles via detected API endpoints")
    if articles:
        print(f"   Sample: {articles[0].get('title', 'N/A')[:50]}...")

    # Test 3: Full scraping with endpoint detection
    print("\n3️⃣ Test: Full scrape with dynamic endpoints (1 domain)")

    results = await scraper.scrape_all_subdomains(
        subdomain_list=["finance.detik.com"], articles_per_subdomain=20
    )

    stats = scraper.get_statistics()

    print(f"\n✅ Full Scraping Results:")
    print(f"  - Total articles: {stats['total_articles']}")
    print(f"  - Per domain: {stats['by_subdomain_count']}")

    # Check endpoint cache
    print(f"\n✅ Endpoint cache: {len(scraper._endpoint_cache)} domains cached")
    for domain, eps in scraper._endpoint_cache.items():
        print(f"  - {domain}: {len(eps)} endpoints")

    print("\n" + "=" * 70)

    # Validation
    success = (
        len(endpoints) >= 15  # Should detect at least 15 endpoints
        and len(recommendation) >= 5  # At least 5 recommendation endpoints
        and stats["total_articles"] >= 10  # At least 10 articles scraped
    )

    if success:
        print("✅ STEP 2 TEST PASSED!")
        print(f"\n📊 Results:")
        print(f"   - Total endpoints detected: {len(endpoints)}")
        print(f"   - Recommendation endpoints: {len(recommendation)}")
        print(f"   - Articles via API: {len(articles)}")
        print(f"   - Total articles scraped: {stats['total_articles']}")
        return True
    else:
        print("❌ STEP 2 TEST FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
