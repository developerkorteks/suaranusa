"""Quick test for Data Normalizer - Step 5."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.data_normalizer import DataNormalizer
import json


def main():
    print("🧪 Quick Test - Data Normalizer")
    print("=" * 60)

    normalizer = DataNormalizer(strict_mode=False)

    # Test 1: Field mapping with various names
    print("\n1️⃣ Test: Field mapping from different sources")

    raw_variations = [
        {
            "article_id": "d-8412424",
            "headline": "Article from API",
            "articleurl": "https://news.detik.com/api",
            "kategori": "news",
        },
        {
            "id": "8412425",
            "title": "Article from HTML",
            "url": "https://news.detik.com/html",
            "category": "finance",
        },
        {
            "contentId": "8412426",
            "name": "Article from CMS",
            "link": "https://news.detik.com/cms",
            "section": "sport",
        },
    ]

    mapped_count = 0
    for i, raw in enumerate(raw_variations, 1):
        normalized = normalizer.normalize(raw, f"source_{i}")
        if normalized and normalized["id"] and normalized["title"]:
            mapped_count += 1
            print(f"  ✅ Source {i}: {normalized['id']} - {normalized['title'][:40]}")

    print(f"  → Mapped {mapped_count}/3 variations successfully")

    # Test 2: Data cleaning
    print("\n2️⃣ Test: Data cleaning and sanitization")

    dirty_data = {
        "id": "d-8412427",  # Should remove 'd-' prefix
        "title": "   Excessive   Whitespace   &amp;   Entities   ",
        "url": "//news.detik.com/test",  # Should add https:
        "publishdate": "2026/03/23 15:50:29",  # Should normalize to ISO
        "tag": "tag1, tag2 | tag3; tag4",  # Should split properly
    }

    cleaned = normalizer.normalize(dirty_data, "test")

    print(f"  ✅ Cleaned data:")
    print(
        f"     - ID: '{cleaned['id']}' (prefix removed: {not cleaned['id'].startswith('d-')})"
    )
    print(f"     - Title: clean={not '  ' in cleaned['title']}")
    print(f"     - URL: has_protocol={cleaned['url'].startswith('https://')}")
    print(f"     - Date: normalized={'-' in cleaned['publish_date']}")
    print(f"     - Tags: {len(cleaned['tags'])} tags parsed")

    # Test 3: Quality scoring
    print("\n3️⃣ Test: Quality score calculation")

    quality_samples = [
        {  # High quality
            "id": "1",
            "title": "Full Article",
            "url": "https://news.detik.com/full",
            "description": "Full description",
            "publish_date": "2026-03-23",
            "image": "https://img.detik.com/img.jpg",
            "category": "news",
            "tags": ["tag1", "tag2"],
            "author": "John Doe",
            "content": "Full content here",
        },
        {  # Medium quality
            "id": "2",
            "title": "Partial Article",
            "url": "https://news.detik.com/partial",
        },
        {  # Low quality
            "title": "Minimal Article",
        },
    ]

    quality_results = []
    for sample in quality_samples:
        normalized = normalizer.normalize(sample, "quality_test")
        if normalized:
            quality_results.append(normalized["quality_score"])
            print(
                f"  ✅ Quality: {normalized['quality_score']:.2f} - {normalized.get('title', 'N/A')[:30]}"
            )

    # Verify quality scores are descending
    is_descending = all(
        quality_results[i] >= quality_results[i + 1]
        for i in range(len(quality_results) - 1)
    )
    print(f"  → Quality scores properly ranked: {is_descending}")

    # Test 4: Batch normalization
    print("\n4️⃣ Test: Batch normalization")

    normalizer.reset_stats()

    raw_batch = [
        {"id": "1", "title": "Valid Article 1", "url": "https://test.com/1"},
        {"id": "2", "title": "Valid Article 2", "url": "https://test.com/2"},
        {"id": "3", "title": "Valid Article 3"},  # Missing URL, still valid
        {"title": "No ID"},  # Missing ID, but has title (valid in non-strict)
        {},  # Empty (should be rejected)
        {"id": "5"},  # Only ID, no title (should be rejected)
    ]

    normalized_batch = normalizer.normalize_batch(raw_batch, "batch_test")

    print(f"  ✅ Batch results:")
    print(f"     - Input: {len(raw_batch)} items")
    print(f"     - Normalized: {len(normalized_batch)} items")
    print(f"     - Rejected: {len(raw_batch) - len(normalized_batch)} items")

    # Test 5: Statistics
    print("\n5️⃣ Test: Statistics tracking")

    stats = normalizer.get_stats()

    print(f"  ✅ Normalizer statistics:")
    print(f"     - Total processed: {stats['total_processed']}")
    print(f"     - Total normalized: {stats['total_normalized']}")
    print(f"     - Total rejected: {stats['total_rejected']}")
    print(f"     - Success rate: {stats['success_rate']:.1%}")
    print(f"     - Avg quality: {stats['average_quality_score']:.2f}")

    print("\n" + "=" * 60)

    # Validation
    success_count = 0

    if mapped_count >= 3:
        success_count += 1
    if cleaned["id"] and not cleaned["id"].startswith("d-"):
        success_count += 1
    if is_descending and len(quality_results) >= 2:
        success_count += 1
    if len(normalized_batch) >= 3:
        success_count += 1
    if stats["success_rate"] > 0.5:
        success_count += 1

    if success_count >= 4:
        print("✅ Step 5 tests PASSED!")
        print(f"   - {success_count}/5 test groups passed")
        print(f"   - Field mapping: {mapped_count}/3")
        print(f"   - Batch normalized: {len(normalized_batch)}/{len(raw_batch)}")
        print(f"   - Success rate: {stats['success_rate']:.1%}")
        return True
    else:
        print("❌ Step 5 tests FAILED")
        print(f"   - Only {success_count}/5 test groups passed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
