"""Full Comprehensive Test - All 20 Content Channels."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from datetime import datetime
from core.comprehensive_scraper import ComprehensiveScraper
from storage.database import Database


async def main():
    print("🧪 FULL COMPREHENSIVE TEST - All Content Channels")
    print("=" * 70)
    print("Testing ALL discovered content channels")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Initialize
    scraper = ComprehensiveScraper(rate_limit=0.5, max_workers=5)
    db = Database("data/comprehensive_full_test.db")
    db.clear_all()

    # Step 1: Discover & filter
    print("1️⃣ Discovering domains...")
    all_domains = await scraper._discover_domains()

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
    print(f"   Testing ALL {len(content_channels)} domains\n")

    print("📊 All content channels to test:")
    for i, domain in enumerate(content_channels, 1):
        print(f"  {i:2}. {domain}")

    print("\n" + "=" * 70)
    print("🚀 Starting FULL comprehensive scraping...")
    print("   This will take 3-5 minutes...\n")

    start_time = datetime.now()

    # Step 2: Scrape ALL domains
    results = await scraper.scrape_all_subdomains(
        subdomain_list=None, articles_per_subdomain=15  # Use discovery!
    )

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Step 3: Statistics
    stats = scraper.get_statistics()

    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE RESULTS")
    print("=" * 70)

    print(f"\n⏱️  Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print(f"✅ Domains discovered: {len(all_domains)}")
    print(f"✅ Content channels: {len(content_channels)}")
    print(f"✅ Domains scraped: {stats['total_subdomains_scraped']}")
    print(f"✅ Total articles: {stats['total_articles']}")
    print(
        f"✅ Avg per domain: {stats['total_articles'] / max(stats['total_subdomains_scraped'], 1):.1f}"
    )

    print("\n📈 Top 10 domains by articles:")
    sorted_domains = sorted(
        stats["by_subdomain_count"].items(), key=lambda x: x[1], reverse=True
    )
    for i, (domain, count) in enumerate(sorted_domains[:10], 1):
        print(f"  {i:2}. {domain:30} : {count:3} articles")

    if len(sorted_domains) > 10:
        print(f"  ... and {len(sorted_domains) - 10} more domains")

    # Step 4: Store in database
    print("\n💾 Storing in database...")
    total_stored = 0
    for domain, data in results["by_subdomain"].items():
        articles = data.get("articles", [])
        if articles:
            stored = db.insert_batch(articles)
            total_stored += stored

    print(f"  ✅ Stored {total_stored} articles")

    # Step 5: Database stats
    db_stats = db.get_statistics()

    print("\n📊 Database Statistics:")
    print(f"  - Total articles: {db_stats['total_articles']}")
    print(f"  - Total tags: {db_stats['total_tags']}")
    print(f"  - Avg quality: {db_stats['average_quality_score']:.2f}")
    print(f"  - Sources: {len(db_stats['by_source'])}")

    # Step 6: Export
    print("\n💾 Exporting to JSON...")
    export_file = "data/comprehensive_full_export.json"
    exported = db.export_to_json(export_file)
    print(f"  ✅ Exported {exported} articles to {export_file}")

    db.close()

    print("\n" + "=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)

    # Performance metrics
    print(f"\n⚡ Performance Metrics:")
    print(f"  - Total time: {duration:.1f}s ({duration/60:.1f} min)")
    print(
        f"  - Time per domain: {duration / max(stats['total_subdomains_scraped'], 1):.1f}s"
    )
    print(f"  - Articles per second: {stats['total_articles'] / duration:.1f}")
    print(
        f"  - Domains per minute: {stats['total_subdomains_scraped'] / (duration/60):.1f}"
    )

    print(f"\n📊 Coverage:")
    print(f"  - All domains: {len(all_domains)}")
    print(f"  - Content channels: {len(content_channels)}")
    print(f"  - Successfully scraped: {stats['total_subdomains_scraped']}")
    print(
        f"  - Coverage: {stats['total_subdomains_scraped'] / len(content_channels) * 100:.1f}%"
    )

    print(f"\n📈 Data Quality:")
    print(f"  - Total articles: {stats['total_articles']}")
    print(f"  - Stored: {total_stored}")
    print(f"  - Exported: {exported}")
    print(f"  - Quality score: {db_stats['average_quality_score']:.2f}")

    # Validation
    success = (
        stats["total_subdomains_scraped"] >= 15
        and stats["total_articles"] >= 200
        and db_stats["average_quality_score"] >= 0.3
        and exported >= 200
    )

    print("\n" + "=" * 70)

    if success:
        print("✅ FULL COMPREHENSIVE TEST PASSED!")
        print("\n🎉 System fully validated:")
        print(f"   - {stats['total_subdomains_scraped']} domains scraped successfully")
        print(f"   - {stats['total_articles']} articles collected")
        print(f"   - {exported} articles exported")
        print(f"   - Quality score: {db_stats['average_quality_score']:.2f}")
        print(f"   - Completed in {duration/60:.1f} minutes")
        return True
    else:
        print("⚠️  TEST COMPLETED WITH WARNINGS")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
