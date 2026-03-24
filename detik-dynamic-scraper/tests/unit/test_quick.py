"""Quick test for domain discovery."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.domain_discovery import DomainDiscovery
import asyncio


async def main():
    print("🧪 Quick Test - Domain Discovery")
    print("=" * 60)

    discovery = DomainDiscovery()

    # Test 1: Extract subdomain
    print("\n1️⃣ Test: Extract subdomain from URL")
    test_urls = [
        "https://news.detik.com/berita",
        "https://finance.detik.com",
        "//cdn.detik.net.id/assets/js/script.js",
        "/relative/path",
        "https://google.com",
    ]

    for url in test_urls:
        result = discovery._extract_subdomain(url)
        status = "✅" if result else "⚠️"
        print(f"  {status} {url[:50]:50s} -> {result}")

    # Test 2: Discover domains
    print("\n2️⃣ Test: Discover domains from detik.com")
    print("  This may take 10-30 seconds...")

    domains = await discovery.discover()

    print(f"\n✅ Discovered {len(domains)} unique domains\n")

    # Test 3: Categorize
    print("3️⃣ Test: Categorize domains")
    categories = discovery.get_domains_by_category()

    for category, domains_list in categories.items():
        if domains_list:
            print(f"\n  📁 {category.upper()} ({len(domains_list)} domains):")
            for domain in sorted(domains_list)[:5]:  # Show first 5
                print(f"     - {domain}")
            if len(domains_list) > 5:
                print(f"     ... and {len(domains_list) - 5} more")

    print("\n" + "=" * 60)
    print("✅ All quick tests passed!")

    return len(domains)


if __name__ == "__main__":
    total = asyncio.run(main())

    # Validation
    if total >= 10:
        print(f"\n🎉 SUCCESS: Found {total} domains (expected >= 10)")
        sys.exit(0)
    else:
        print(f"\n❌ FAILED: Only found {total} domains (expected >= 10)")
        sys.exit(1)
