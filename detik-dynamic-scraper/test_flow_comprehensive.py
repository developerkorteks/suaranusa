import requests
import time
import json
from typing import List, Dict

API_BASE = "http://localhost:8000"

DOMAINS = [
    "https://news.detik.com",
    "https://finance.detik.com",
    "https://hot.detik.com",
    "https://inet.detik.com",
    "https://sport.detik.com",
    "https://oto.detik.com",
    "https://travel.detik.com",
    "https://health.detik.com",
    "https://wolipop.detik.com",
    "https://20.detik.com",
]


def scrape_domain(url: str):
    print(f"Scraping Domain: {url}")
    try:
        response = requests.post(
            f"{API_BASE}/api/scrape", json={"url": url}, timeout=30
        )
        data = response.json()
        print(
            f"Scraped: {data.get('articles_scraped', 0)}, Saved: {data.get('articles_saved', 0)}"
        )
        return data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def get_articles_for_domain(domain_fragment: str, limit: int = 20) -> List[Dict]:
    print(f"Fetching up to {limit} articles for {domain_fragment}...")
    try:
        response = requests.post(
            f"{API_BASE}/api/articles/search",
            json={"source": domain_fragment, "limit": limit},
        )
        data = response.json()
        return data.get("articles", [])
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []


def scrape_article_detail(article_id: str):
    try:
        response = requests.post(
            f"{API_BASE}/api/articles/{article_id}/scrape-detail", timeout=20
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    print("Starting Comprehensive Testing Flow...")
    results = {}
    for domain in DOMAINS:
        domain_name = domain.replace("https://", "")
        scrape_domain(domain)
        time.sleep(1)
        articles = get_articles_for_domain(domain, limit=20)
        print(f"Found {len(articles)} articles for {domain_name}")
        detail_success = 0
        for article in articles:
            article_id = article["id"]
            res = scrape_article_detail(article_id)
            if res.get("success"):
                detail_success += 1
            time.sleep(0.1)
        print(
            f"Completed {domain_name}: {detail_success}/{len(articles)} details scraped."
        )
        results[domain_name] = {
            "total_found": len(articles),
            "detail_success": detail_success,
        }
    print("\nFINAL TEST SUMMARY")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
