import asyncio
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from core.content_scraper import ContentScraper
from core.data_normalizer import DataNormalizer

async def test_flow():
    scraper = ContentScraper()
    normalizer = DataNormalizer()
    
    # URL target (Detik News)
    url = "https://news.detik.com/berita/d-8414162/iran-siap-kawal-kapal-lintasi-selat-hormuz-setelah-serangan-israel"
    
    print(f"--- STEP 1: Scrape Raw URL: {url} ---")
    articles = await scraper.scrape(url, response_type="html")
    
    if not articles:
        print("Gagal scrape artikel!")
        return

    raw_article = articles[0]
    print(f"RAW CATEGORY FROM SCRAPER: {raw_article.get('category')}")
    
    print("\n--- STEP 2: Normalization ---")
    # Simulate normalizer call in ScraperService
    normalized_articles = normalizer.normalize_batch(articles, source=url)
    
    if not normalized_articles:
        print("Gagal normalisasi!")
        return
        
    norm_article = normalized_articles[0]
    print(f"NORMALIZED CATEGORY: {norm_article.get('category')}")
    print(f"NORMALIZED SOURCE: {norm_article.get('source')}")
    
    print("\n--- STEP 3: Final Object for DB ---")
    # Only show essential fields to avoid noise
    final_output = {
        "id": norm_article.get("id"),
        "title": norm_article.get("title")[:60] + "...",
        "category": norm_article.get("category"),
        "source": norm_article.get("source"),
        "url": norm_article.get("url")[:60] + "..."
    }
    print(json.dumps(final_output, indent=2))

if __name__ == "__main__":
    asyncio.run(test_flow())
