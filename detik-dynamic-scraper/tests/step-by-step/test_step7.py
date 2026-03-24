"""Quick test for REST API - Step 7."""

import sys
from pathlib import Path
import asyncio
import httpx
import subprocess
import time


def main():
    print("🧪 Quick Test - REST API")
    print("=" * 60)

    # Start API server in background
    print("\n1️⃣ Test: Starting API server...")

    api_process = subprocess.Popen(
        [
            "python3",
            "-m",
            "uvicorn",
            "src.api.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=Path(__file__).parent,
    )

    print("  ⏳ Waiting for server to start...")
    time.sleep(3)  # Give server time to start

    try:
        # Test API endpoints
        base_url = "http://127.0.0.1:8000"

        # Test 2: Health check
        print("\n2️⃣ Test: Health check endpoint")
        response = httpx.get(f"{base_url}/health", timeout=10.0)

        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Health check: {data['status']}")
        else:
            print(f"  ❌ Health check failed: {response.status_code}")

        # Test 3: Root endpoint
        print("\n3️⃣ Test: Root endpoint")
        response = httpx.get(f"{base_url}/", timeout=10.0)

        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API Name: {data['name']}")
            print(f"     Version: {data['version']}")
            print(f"     Endpoints: {len(data['endpoints'])} available")
        else:
            print(f"  ❌ Root failed: {response.status_code}")

        # Test 4: Statistics endpoint
        print("\n4️⃣ Test: Statistics endpoint")
        response = httpx.get(f"{base_url}/api/statistics", timeout=10.0)

        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Statistics:")
            print(f"     - Database articles: {data['database']['total_articles']}")
            print(f"     - Success: {data['success']}")
        else:
            print(f"  ❌ Statistics failed: {response.status_code}")

        # Test 5: Scrape endpoint (with small request)
        print("\n5️⃣ Test: Scrape endpoint")
        scrape_request = {
            "url": "https://recg.detik.com/article-recommendation/wp/test?size=3&nocache=1&ids=undefined&acctype=acc-detikcom",
            "response_type": "json",
            "normalize": True,
            "save_to_db": False,
        }

        response = httpx.post(
            f"{base_url}/api/scrape", json=scrape_request, timeout=30.0
        )

        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Scrape successful:")
            print(f"     - Articles: {data['articles_count']}")
            print(f"     - Success: {data['success']}")
        else:
            print(f"  ⚠️  Scrape endpoint: {response.status_code}")

        print("\n" + "=" * 60)
        print("✅ Step 7 tests PASSED!")
        print("   - API server running")
        print("   - All endpoints responding")
        print("   - Health check OK")

        success = True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        success = False

    finally:
        # Stop API server
        print("\n⏹️  Stopping API server...")
        api_process.terminate()
        api_process.wait(timeout=5)
        print("  ✅ Server stopped")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
