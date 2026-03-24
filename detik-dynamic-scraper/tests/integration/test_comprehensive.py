"""Test Comprehensive Scraper - All Subdomains."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from core.comprehensive_scraper import ComprehensiveScraper
from storage.database import Database


async def main():
    print("🧪 Comprehensive Scraper Test - All Subdomains")
    print("=" * 70)

    # Initialize
    scraper = ComprehensiveScraper(rate_limit=0.5, max_workers=5)
    db = Database("data/comprehensive_test.db")
    db.clear_all()

    # Test with all main content channels (15 subdomains)
    print("\n📊 Testing with 15 main content subdomains")
    print("   This will take ~30-60 seconds...\n")

    results = await scraper.scrape_all_subdomains(
        subdomain_list=scraper.ALL_SUBDOMAINS, articles_per_subdomain=20
    )

    # Get statistics
    stats = scraper.get_statistics()

    print("\n" + "=" * 70)
    print("📊 SCRAPING RESULTS")
    print("=" * 70)

    print(f"\n✅ Subdomains Scraped: {stats['total_subdomains_scraped']}")
    print(f"✅ Total Articles: {stats['total_articles']}")

    print("\n📈 Articles per Subdomain:")
    for subdomain, count in sorted(
        stats["by_subdomain_count"].items(), key=lambda x: x[1], reverse=True
    ):
        print(f"  - {subdomain:25} : {count:3} articles")

    # Store in database
    print("\n💾 Storing in database...")
    total_stored = 0
    for subdomain, data in results["by_subdomain"].items():
        articles = data.get("articles", [])
        if articles:
            stored = db.insert_batch(articles)
            total_stored += stored

    print(f"  ✅ Stored {total_stored} articles in database")

    # Scrape Terpopuler
    print("\n📈 Scraping Terpopuler pages...")
    terpopuler = await scraper.scrape_terpopuler()
    if terpopuler:
        db.insert_batch(terpopuler)
        print(f"  ✅ Scraped {len(terpopuler)} articles from Terpopuler")

    # Final database stats
    db_stats = db.get_statistics()

    print("\n" + "=" * 70)
    print("📊 DATABASE STATISTICS")
    print("=" * 70)
    print(f"  - Total articles in DB: {db_stats['total_articles']}")
    print(f"  - Total tags: {db_stats['total_tags']}")
    print(f"  - Average quality: {db_stats['average_quality_score']:.2f}")
    print(f"  - By source: {len(db_stats['by_source'])} sources")
    print(f"  - By category: {len(db_stats['by_category'])} categories")

    # Export
    print("\n💾 Exporting to JSON...")
    exported = db.export_to_json("data/comprehensive_export.json")
    print(f"  ✅ Exported {exported} articles")

    db.close()

    print("\n" + "=" * 70)

    # Validation
    success = (
        stats["total_articles"] >= 100
        and stats["total_subdomains_scraped"] >= 10
        and db_stats["total_articles"] >= 100
    )

    if success:
        print("✅ COMPREHENSIVE TEST PASSED!")
        print(f"\n🎉 Summary:")
        print(f"   - {stats['total_subdomains_scraped']} subdomains scraped")
        print(f"   - {stats['total_articles']} articles collected")
        print(f"   - {db_stats['total_articles']} articles in database")
        print(f"   - {len(terpopuler)} trending articles")
        print(f"   - {exported} articles exported")
        return True
    else:
        print("❌ COMPREHENSIVE TEST FAILED")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
