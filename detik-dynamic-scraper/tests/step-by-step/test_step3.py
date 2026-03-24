"""Quick test for Parameter Extraction - Step 3."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.parameter_extractor import ParameterExtractor
import asyncio
import json


async def main():
    print("🧪 Quick Test - Parameter Extraction")
    print("=" * 60)

    extractor = ParameterExtractor()

    # Test 1: Extract parameters from news.detik.com
    print("\n1️⃣ Test: Extract parameters from news.detik.com")
    print("  This may take 5-10 seconds...\n")

    params = await extractor.extract(
        "news.detik.com", "https://rech.detik.com/article-recommendation/detail/"
    )

    print(f"  ✅ Extracted {len(params)} parameters:")
    for key, value in params.items():
        print(f"     - {key}: {value}")

    # Test 2: Verify key parameters
    print("\n2️⃣ Test: Verify key parameters exist")

    required_params = ["acctype", "size", "nocache", "ids"]
    found_params = []

    for param in required_params:
        if param in params:
            found_params.append(param)
            print(f"  ✅ Found {param}: {params[param]}")
        else:
            print(f"  ⚠️  {param} not found")

    # Test 3: Build parameter schema
    print("\n3️⃣ Test: Build parameter schema")

    schema = extractor.build_parameter_schema(
        "https://rech.detik.com/article-recommendation/detail/", params
    )

    print(f"  ✅ Schema created:")
    print(f"     - Required params: {schema['required']}")
    print(f"     - Optional params: {schema['optional'][:5]}")  # Show first 5
    print(f"     - Defaults: {len(schema['defaults'])} values")

    # Test 4: Generate parameters with overrides
    print("\n4️⃣ Test: Generate parameters with overrides")

    generated = extractor.generate_params(
        "news.detik.com",
        "https://rech.detik.com/article-recommendation/detail/",
        {"size": 20, "custom_param": "test"},
    )

    print(f"  ✅ Generated {len(generated)} parameters")
    print(f"     - Size override: {generated.get('size')}")
    print(f"     - Custom param: {generated.get('custom_param')}")

    # Test 5: Test multiple domains
    print("\n5️⃣ Test: Extract from multiple domains")

    test_domains = ["finance.detik.com", "sport.detik.com", "hot.detik.com"]
    acctype_results = {}

    for domain in test_domains:
        params = await extractor.extract(
            domain, "https://rech.detik.com/article-recommendation/wp/"
        )
        acctype_results[domain] = params.get("acctype", "NOT_FOUND")
        print(f"  ✅ {domain}: {acctype_results[domain]}")

    print("\n" + "=" * 60)

    # Validation
    success_count = 0

    if len(params) >= 3:
        success_count += 1
    if len(found_params) >= 3:
        success_count += 1
    if schema and len(schema.get("optional", [])) > 0:
        success_count += 1
    if generated.get("size") == 20:
        success_count += 1
    if len(acctype_results) == 3:
        success_count += 1

    if success_count >= 4:
        print("✅ Step 3 tests PASSED!")
        print(f"   - {success_count}/5 test groups passed")
        print(f"   - {len(params)} parameters extracted")
        print(f"   - {len(found_params)}/{len(required_params)} required params found")
        return True
    else:
        print("❌ Step 3 tests FAILED")
        print(f"   - Only {success_count}/5 test groups passed")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
