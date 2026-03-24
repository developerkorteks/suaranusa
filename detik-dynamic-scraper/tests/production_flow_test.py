import asyncio
import sys
import os
import time
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.article_detail_scraper import ArticleDetailScraper
from core.content_scraper import ContentScraper
from core.domain_discovery import DomainDiscovery
from storage.database import Database
from repositories.article_repository import ArticleRepository
from services.scraper_service import ScraperService


async def run_production_flow_test():
    """
    Automated test simulating a production news environment flow.
    """
    print("DETIK DYNAMIC SCRAPER - PRODUCTION FLOW INTEGRATION TEST")
    print("-" * 60)

    BASE_DIR = Path(__file__).parent.parent
    DB_PATH = BASE_DIR / "data" / "comprehensive_full_test.db"
    db = Database(str(DB_PATH))
    repo = ArticleRepository(db)
    scraper_service = ScraperService(repo)
    detail_scraper = ArticleDetailScraper(rate_limit=0.1)
    list_scraper = ContentScraper(rate_limit=0.1)

    # 1. Domain Discovery
    discovery = DomainDiscovery()
    domains = await discovery.discover()
    content_domains = [
        d
        for d in sorted(domains)
        if "detik.com" in d
        and not any(x in d for x in ["cdn", "static", "api", "analytic"])
    ]

    print("Phase 1: Discovered {} content domains.".format(len(content_domains)))

    summary_results = []

    # 2. Process each domain (Limit to 20 articles each)
    for domain in content_domains:
        print("\nProcessing Domain: {}".format(domain))
        start_time = time.time()

        try:
            target_url = "https://{}".format(domain)
            discovered_articles = await list_scraper.scrape(target_url)

            targets = discovered_articles[:20]
            print("   - Found {} articles on list page.".format(len(targets)))

            success_count = 0
            media_total = 0

            for article in targets:
                url = article.get("url")
                if not url:
                    continue

                detail = await detail_scraper.scrape_article_detail(url)
                if detail and detail.get("content"):
                    detail["id"] = article.get("id") or detail.get("id")
                    detail["source"] = domain
                    repo.save(detail)

                    success_count += 1
                    media_total += len(detail.get("images", [])) + len(
                        detail.get("videos", [])
                    )

            duration = time.time() - start_time
            print(
                "   - Result: {}/{} hydrated successfully.".format(
                    success_count, len(targets)
                )
            )
            print("   - Total Media Extracted: {}".format(media_total))
            print("   - Duration: {:.2f}s".format(duration))

            summary_results.append(
                {
                    "domain": domain,
                    "total": len(targets),
                    "success": success_count,
                    "media": media_total,
                    "rate": (success_count / len(targets) * 100) if targets else 0,
                }
            )

        except Exception as e:
            print("   - Error processing {}: {}".format(domain, e))

    # 3. Final Summary
    print("\n" + "=" * 60)
    print("PRODUCTION FLOW TEST SUMMARY")
    print("=" * 60)
    header = "{:<25} | {:<10} | {:<8} | {:<6}".format(
        "DOMAIN", "SUCCESS", "MEDIA", "RATE"
    )
    print(header)
    print("-" * 60)

    overall_total = 0
    overall_success = 0

    for res in summary_results:
        line = "{:<25} | {:>2}/{:<7} | {:<8} | {:.1f}%".format(
            res["domain"], res["success"], res["total"], res["media"], res["rate"]
        )
        print(line)
        overall_total += res["total"]
        overall_success += res["success"]

    print("-" * 60)
    final_rate = (overall_success / overall_total * 100) if overall_total else 0
    print(
        "OVERALL TOTAL: {}/{} articles hydrated ({:.1f}%)".format(
            overall_success, overall_total, final_rate
        )
    )
    print("=" * 60)

    db.close()


if __name__ == "__main__":
    asyncio.run(run_production_flow_test())
