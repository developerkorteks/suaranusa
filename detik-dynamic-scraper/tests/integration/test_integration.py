"""
Integration Test - Full System Test

Tests the complete workflow from domain discovery to data export.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from core.domain_discovery import DomainDiscovery
from core.endpoint_detector import EndpointDetector
from core.parameter_extractor import ParameterExtractor
from core.content_scraper import ContentScraper
from core.data_normalizer import DataNormalizer
from storage.database import Database


async def test_full_workflow():
    """Test complete scraping workflow."""
    print("🧪 Integration Test - Full Workflow")
    print("=" * 70)

    # Initialize components
    db = Database("data/integration_test.db")
    db.clear_all()

    discovery = DomainDiscovery()
    detector = EndpointDetector()
    extractor = ParameterExtractor()
    scraper = ContentScraper(rate_limit=0.5)
    normalizer = DataNormalizer()

    # Step 1: Discover domains
    print("\n1️⃣ Domain Discovery")
    print("  ⏳ Discovering domains...")
    domains = await discovery.discover()
    print(f"  ✅ Found {len(domains)} domains")
    print(f"     Sample: {list(sorted(domains))[:3]}")

    # Step 2: Detect endpoints from one domain
    print("\n2️⃣ Endpoint Detection")
    print("  ⏳ Detecting endpoints from news.detik.com...")
    endpoints = await detector.detect("news.detik.com")
    print(f"  ✅ Found {len(endpoints)} endpoints")
    print(f"     Sample: {list(sorted(endpoints))[:3]}")

    # Step 3: Extract parameters
    print("\n3️⃣ Parameter Extraction")
    print("  ⏳ Extracting parameters for news.detik.com...")
    params = await extractor.extract(
        "news.detik.com", "https://rech.detik.com/article-recommendation/wp/"
    )
    print(f"  ✅ Extracted {len(params)} parameters")
    print(f"     - acctype: {params.get('acctype')}")
    print(f"     - size: {params.get('size')}")

    # Step 4: Scrape content
    print("\n4️⃣ Content Scraping")
    print("  ⏳ Scraping from API endpoint...")
    articles = await scraper.scrape(
        "https://recg.detik.com/article-recommendation/wp/test?size=10&nocache=1&ids=undefined&acctype=acc-detikcom",
        response_type="json",
    )
    print(f"  ✅ Scraped {len(articles)} articles")
    if articles:
        print(f"     Sample: {articles[0].get('title', 'N/A')[:50]}...")

    # Step 5: Normalize data
    print("\n5️⃣ Data Normalization")
    print("  ⏳ Normalizing articles...")
    normalized = normalizer.normalize_batch(articles, "integration_test")
    norm_stats = normalizer.get_stats()
    print(f"  ✅ Normalized {len(normalized)} articles")
    print(f"     - Success rate: {norm_stats['success_rate']:.1%}")
    print(f"     - Avg quality: {norm_stats['average_quality_score']:.2f}")

    # Step 6: Store in database
    print("\n6️⃣ Database Storage")
    print("  ⏳ Storing articles...")
    stored = db.insert_batch(normalized)
    print(f"  ✅ Stored {stored} articles")

    # Step 7: Query and export
    print("\n7️⃣ Query & Export")
    print("  ⏳ Querying database...")

    # Search
    results = db.search_articles(limit=5)
    print(f"  ✅ Query results: {len(results)} articles")

    # Statistics
    stats = db.get_statistics()
    print(f"  ✅ Database stats:")
    print(f"     - Total articles: {stats['total_articles']}")
    print(f"     - Total tags: {stats['total_tags']}")
    print(f"     - Avg quality: {stats['average_quality_score']:.2f}")

    # Export
    exported = db.export_to_json("data/integration_export.json")
    print(f"  ✅ Exported {exported} articles to JSON")

    db.close()

    print("\n" + "=" * 70)

    # Validation
    success_criteria = [
        len(domains) >= 10,
        len(endpoints) >= 5,
        len(params) >= 3,
        len(articles) >= 5,
        len(normalized) >= 5,
        stored >= 5,
        stats["total_articles"] >= 5,
    ]

    passed = sum(success_criteria)
    total = len(success_criteria)

    if passed == total:
        print(f"✅ Integration Test PASSED! ({passed}/{total} criteria met)")
        print("\n📊 Final Results:")
        print(f"   - Domains discovered: {len(domains)}")
        print(f"   - Endpoints detected: {len(endpoints)}")
        print(f"   - Articles scraped: {len(articles)}")
        print(f"   - Articles normalized: {len(normalized)}")
        print(f"   - Articles stored: {stored}")
        print(f"   - Export successful: Yes")
        return True
    else:
        print(f"❌ Integration Test FAILED ({passed}/{total} criteria met)")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_full_workflow())
    sys.exit(0 if success else 1)
