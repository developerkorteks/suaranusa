import asyncio
import json
import sys
import os
from pathlib import Path
from urllib.parse import urlparse

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.content_scraper import ContentScraper
from core.data_normalizer import DataNormalizer

async def test_domain(scraper, normalizer, domain, url):
    print(f"TESTING {domain}...")
    
    try:
        articles = await scraper.scrape(url, response_type="auto")
        if not articles:
            return None

        raw = articles[0]
        # Important: ScraperService calls normalizer.normalize_batch(articles, source=url)
        normalized = normalizer.normalize(raw, source=url)
        
        return {
            "domain": domain,
            "raw_category": raw.get("category"),
            "norm_category": normalized.get("category") if normalized else "FAILED",
            "norm_source": normalized.get("source") if normalized else "FAILED",
            "sample_url": raw.get("url")[:60] + "..." if raw.get("url") else "NONE"
        }
    except Exception as e:
        print(f"Error testing {domain}: {e}")
        return None

async def main():
    scraper = ContentScraper(rate_limit=0.5)
    normalizer = DataNormalizer()
    
    test_targets = [
        ("NEWS", "https://news.detik.com"),
        ("FINANCE", "https://finance.detik.com"),
        ("SPORT", "https://sport.detik.com"),
        ("VIDEO", "https://20.detik.com"),
        ("HEALTH", "https://health.detik.com"),
        ("HOT", "https://hot.detik.com"),
        ("INET", "https://inet.detik.com"),
        ("WOLIPOP", "https://wolipop.detik.com")
    ]
    
    results = []
    for domain, url in test_targets:
        res = await test_domain(scraper, normalizer, domain, url)
        if res:
            results.append(res)
            
    print("\n" + "="*80)
    print(f"{'DOMAIN':<10} | {'RAW CAT':<10} | {'NORM CAT':<10} | {'SOURCE'}")
    print("-" * 100)
    for r in results:
        # Truncate source for table display
        src = r['norm_source']
        if len(src) > 40: src = src[:37] + "..."
        print(f"{r['domain']:<10} | {str(r['raw_category']):<10} | {str(r['norm_category']):<10} | {src}")

if __name__ == "__main__":
    asyncio.run(main())
