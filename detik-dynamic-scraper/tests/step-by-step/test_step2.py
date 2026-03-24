"""Quick test for API Endpoint Detection - Step 2."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.endpoint_detector import EndpointDetector
import asyncio


async def main():
    print("🧪 Quick Test - API Endpoint Detection")
    print("=" * 60)

    detector = EndpointDetector()

    # Test 1: Detect from news.detik.com
    print("\n1️⃣ Test: Detect endpoints from news.detik.com")
    print("  This may take 15-30 seconds...\n")

    endpoints = await detector.detect("news.detik.com")

    print(f"\n✅ Detected {len(endpoints)} API endpoints")

    # Test 2: Categorize endpoints
    print("\n2️⃣ Test: Categorize endpoints by type")
    categories = detector.categorize_endpoints()

    for category, endpoint_list in categories.items():
        if endpoint_list:
            print(
                f"\n  📁 {category.upper().replace('_', ' ')} ({len(endpoint_list)} endpoints):"
            )
            for endpoint in sorted(endpoint_list)[:3]:  # Show first 3
                print(f"     - {endpoint}")
            if len(endpoint_list) > 3:
                print(f"     ... and {len(endpoint_list) - 3} more")

    # Test 3: Verify key endpoints found
    print("\n3️⃣ Test: Verify key API endpoints found")

    key_patterns = ["recommendation", "rech", "recg", "connect", "comment"]
    found_patterns = []

    for pattern in key_patterns:
        if any(pattern in e for e in endpoints):
            found_patterns.append(pattern)
            print(f"  ✅ Found {pattern} endpoint")
        else:
            print(f"  ⚠️  {pattern} endpoint not found")

    print("\n" + "=" * 60)

    if len(endpoints) >= 5 and len(found_patterns) >= 2:
        print("✅ Step 2 tests PASSED!")
        print(f"   - {len(endpoints)} endpoints detected")
        print(f"   - {len(found_patterns)}/{len(key_patterns)} key patterns found")
        return True
    else:
        print("❌ Step 2 tests FAILED")
        print(f"   - Only {len(endpoints)} endpoints (expected >= 5)")
        print(f"   - Only {len(found_patterns)} key patterns (expected >= 2)")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
