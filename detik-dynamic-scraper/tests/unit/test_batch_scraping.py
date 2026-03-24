"""Batch Test - Incremental Domain Testing."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
import argparse
from core.comprehensive_scraper import ComprehensiveScraper
from storage.database import Database


async def main(batch_size=5, articles_per_domain=10):
    print("🧪 BATCH TEST - Comprehensive Scraping")
    print("=" * 70)
    print(f"Batch size: {batch_size} domains")
    print(f"Target: {articles_per_domain} articles per domain\n")

    # Initialize
    scraper = ComprehensiveScraper(rate_limit=0.5, max_workers=3)
    db = Database("data/batch_test.db")

    # Step 1: Discover domains
    print("1️⃣ Discovering domains...")
    all_domains = await scraper._discover_domains()

    # Filter to content channels
    content_channels = sorted(
        [
            d
            for d in all_domains
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

    print(f"✅ Found {len(content_channels)} content channels")
    print(f"   Testing first {batch_size} domains\n")

    # Select batch
    test_domains = content_channels[:batch_size]

    print("📊 Domains to test:")
    for i, domain in enumerate(test_domains, 1):
        print(f"  {i:2}. {domain}")

    print("\n" + "=" * 70)
    print("🚀 Starting batch scraping...\n")

    # Step 2: Scrape batch
    results = await scraper.scrape_all_subdomains(
        subdomain_list=test_domains, articles_per_subdomain=articles_per_domain
    )

    # Step 3: Get statistics
    stats = scraper.get_statistics()

    print("\n" + "=" * 70)
    print("📊 BATCH RESULTS")
    print("=" * 70)

    print(f"\n✅ Domains processed: {stats['total_subdomains_scraped']}/{batch_size}")
    print(f"✅ Total articles: {stats['total_articles']}")
    print(
        f"✅ Average per domain: {stats['total_articles'] / max(stats['total_subdomains_scraped'], 1):.1f}"
    )

    print("\n📈 Articles per domain:")
    for domain, count in sorted(
        stats["by_subdomain_count"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"  - {domain:30} : {count:3} articles")

    # Step 4: Store in database
    print("\n💾 Storing in database...")
    total_stored = 0
    for domain, data in results["by_subdomain"].items():
        articles = data.get("articles", [])
        if articles:
            stored = db.insert_batch(articles)
            total_stored += stored

    print(f"  ✅ Stored {total_stored} articles")

    # Step 5: Database statistics
    db_stats = db.get_statistics()

    print("\n📊 Database Statistics:")
    print(f"  - Total articles: {db_stats['total_articles']}")
    print(f"  - Total tags: {db_stats['total_tags']}")
    print(f"  - Avg quality: {db_stats['average_quality_score']:.2f}")

    # Step 6: Export
    print("\n💾 Exporting to JSON...")
    export_file = f"data/batch_{batch_size}_export.json"
    exported = db.export_to_json(export_file)
    print(f"  ✅ Exported {exported} articles to {export_file}")

    db.close()

    print("\n" + "=" * 70)

    # Validation
    success_rate = stats["total_subdomains_scraped"] / batch_size
    articles_ok = stats["total_articles"] >= (batch_size * 0.5 * articles_per_domain)
    quality_ok = db_stats["average_quality_score"] >= 0.3

    if success_rate >= 0.8 and articles_ok and quality_ok:
        print("✅ BATCH TEST PASSED!")
        print(f"\n📊 Summary:")
        print(f"   - Success rate: {success_rate:.1%}")
        print(f"   - Total articles: {stats['total_articles']}")
        print(f"   - Quality score: {db_stats['average_quality_score']:.2f}")
        print(f"   - Exported: {exported} articles")
        return True
    else:
        print("⚠️  BATCH TEST COMPLETED WITH WARNINGS")
        print(f"   - Success rate: {success_rate:.1%}")
        print(f"   - Articles scraped: {stats['total_articles']}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch test scraping")
    parser.add_argument(
        "--batch", type=int, default=5, help="Number of domains to test (default: 5)"
    )
    parser.add_argument(
        "--articles",
        type=int,
        default=10,
        help="Target articles per domain (default: 10)",
    )

    args = parser.parse_args()

    success = asyncio.run(main(args.batch, args.articles))
    sys.exit(0 if success else 1)
