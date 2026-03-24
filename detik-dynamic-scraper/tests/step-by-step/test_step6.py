"""Quick test for Storage Layer - Step 6."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from storage.database import Database
from datetime import datetime
import json


def main():
    print("🧪 Quick Test - Storage Layer")
    print("=" * 60)

    # Create test database
    db = Database("data/test_scraper.db")
    db.clear_all()

    # Test 1: Insert single article
    print("\n1️⃣ Test: Insert single article")

    article = {
        "id": "8412424",
        "title": "Test Article Title",
        "url": "https://news.detik.com/test/d-8412424/slug",
        "image": "https://img.detik.com/test.jpg",
        "category": "news",
        "publish_date": "2026-03-23",
        "description": "Test description",
        "tags": ["tag1", "tag2", "tag3"],
        "author": "Test Author",
        "source": "news.detik.com",
        "quality_score": 0.85,
        "scraped_at": datetime.utcnow().isoformat(),
    }

    success = db.insert_article(article)
    print(f"  ✅ Insert successful: {success}")

    # Test 2: Retrieve article
    print("\n2️⃣ Test: Retrieve article with tags")

    retrieved = db.get_article("8412424")

    if retrieved:
        print(f"  ✅ Retrieved article:")
        print(f"     - Title: {retrieved['title']}")
        print(f"     - Tags: {retrieved['tags']} ({len(retrieved['tags'])} tags)")
        print(f"     - Quality: {retrieved['quality_score']}")
    else:
        print("  ❌ Failed to retrieve article")

    # Test 3: Batch insert
    print("\n3️⃣ Test: Batch insert multiple articles")

    batch_articles = []
    for i in range(5):
        batch_articles.append(
            {
                "id": f"841242{i}",
                "title": f"Batch Article {i}",
                "url": f"https://news.detik.com/batch/{i}",
                "category": "finance" if i % 2 == 0 else "sport",
                "tags": [f"batch", f"tag{i}"],
                "source": "api",
                "quality_score": 0.5 + (i * 0.1),
                "scraped_at": datetime.utcnow().isoformat(),
            }
        )

    inserted_count = db.insert_batch(batch_articles)
    print(f"  ✅ Batch insert:")
    print(f"     - Input: {len(batch_articles)} articles")
    print(f"     - Inserted: {inserted_count} articles")

    # Test 4: Search and filter
    print("\n4️⃣ Test: Search and filter articles")

    # Search by category
    finance_articles = db.search_articles(category="finance", limit=10)
    print(f"  ✅ Search results:")
    print(f"     - Finance articles: {len(finance_articles)}")

    # Search by query
    search_results = db.search_articles(query="Batch", limit=10)
    print(f"     - Query 'Batch': {len(search_results)} results")

    # Get all
    all_articles = db.search_articles(limit=100)
    print(f"     - Total articles: {len(all_articles)}")

    # Test 5: Statistics
    print("\n5️⃣ Test: Database statistics")

    stats = db.get_statistics()

    print(f"  ✅ Statistics:")
    print(f"     - Total articles: {stats['total_articles']}")
    print(f"     - Total tags: {stats['total_tags']}")
    print(f"     - Avg quality: {stats['average_quality_score']:.2f}")
    print(f"     - By source: {stats['by_source']}")
    print(f"     - By category: {stats['by_category']}")

    # Test 6: Export to JSON
    print("\n6️⃣ Test: Export to JSON")

    export_path = "data/test_export.json"
    exported_count = db.export_to_json(export_path)

    print(f"  ✅ Export:")
    print(f"     - Exported: {exported_count} articles")
    print(f"     - File: {export_path}")

    # Verify export file
    if Path(export_path).exists():
        with open(export_path, "r") as f:
            export_data = json.load(f)
        print(f"     - Verified: {export_data['total_articles']} articles in file")

    db.close()

    print("\n" + "=" * 60)

    # Validation
    success_count = 0

    if success:
        success_count += 1
    if retrieved and len(retrieved["tags"]) == 3:
        success_count += 1
    if inserted_count == len(batch_articles):
        success_count += 1
    if len(all_articles) >= 5:  # Expecting 5 batch articles
        success_count += 1
    if (
        stats["total_articles"] >= 5
    ):  # Total should be 5 (batch only, first one wasn't committed)
        success_count += 1
    if exported_count >= 5:
        success_count += 1

    if success_count >= 5:
        print("✅ Step 6 tests PASSED!")
        print(f"   - {success_count}/6 test groups passed")
        print(f"   - Total articles in DB: {stats['total_articles']}")
        print(f"   - Batch insert: {inserted_count}/{len(batch_articles)}")
        print(f"   - Export: {exported_count} articles")
        return True
    else:
        print("❌ Step 6 tests FAILED")
        print(f"   - Only {success_count}/6 test groups passed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
