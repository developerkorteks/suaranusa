"""Test Step 1: Domain Discovery Integration."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from core.comprehensive_scraper import ComprehensiveScraper


async def main():
    print("🧪 TEST STEP 1: Domain Discovery Integration")
    print("=" * 70)

    scraper = ComprehensiveScraper(rate_limit=0.5, max_workers=3)

    # Test 1: Check if discovery works
    print("\n1️⃣ Test: Domain Discovery")
    domains = await scraper._discover_domains()

    print(f"\n✅ Discovered {len(domains)} domains:")
    for i, domain in enumerate(sorted(domains)[:10], 1):
        print(f"  {i:2}. {domain}")
    if len(domains) > 10:
        print(f"  ... and {len(domains) - 10} more")

    # Test 2: Check filtering (content channels only)
    print("\n2️⃣ Test: Filter to content channels")
    content_channels = sorted(
        [
            d
            for d in domains
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

    print(f"\n✅ Content channels: {len(content_channels)}")
    for i, domain in enumerate(content_channels, 1):
        print(f"  {i:2}. {domain}")

    # Test 3: Test scraping with discovered domains (3 domains only)
    print("\n3️⃣ Test: Scrape with discovered domains (3 samples)")
    test_domains = content_channels[:3]

    results = await scraper.scrape_all_subdomains(
        subdomain_list=test_domains, articles_per_subdomain=10
    )

    stats = scraper.get_statistics()

    print(f"\n✅ Scraping Results:")
    print(f"  - Domains scraped: {stats['total_subdomains_scraped']}")
    print(f"  - Total articles: {stats['total_articles']}")
    print(f"  - Per domain: {stats['by_subdomain_count']}")

    print("\n" + "=" * 70)

    # Validation
    success = (
        len(domains) >= 25  # Should find at least 25 domains
        and len(content_channels) >= 10  # At least 10 content channels
        and stats["total_articles"] >= 10  # At least 10 articles scraped
    )

    if success:
        print("✅ STEP 1 TEST PASSED!")
        print(f"\n📊 Results:")
        print(f"   - Total domains discovered: {len(domains)}")
        print(f"   - Content channels: {len(content_channels)}")
        print(f"   - Articles scraped: {stats['total_articles']}")
        print(f"   - Domains tested: {len(test_domains)}")
        return True
    else:
        print("❌ STEP 1 TEST FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
