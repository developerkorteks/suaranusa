#!/usr/bin/env python3
"""
Detik.com API Scraper - Complete Flow Analysis
Mengambil semua data dari berbagai endpoint API detik.com
"""

import requests
import json
import re
from datetime import datetime
from typing import List, Dict, Any
import time


class DetikAPIScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.detik.com/",
        }
        self.base_urls = {
            "main": "https://www.detik.com",
            "news": "https://news.detik.com",
            "finance": "https://finance.detik.com",
            "sport": "https://sport.detik.com",
            "hot": "https://hot.detik.com",
            "inet": "https://inet.detik.com",
            "travel": "https://travel.detik.com",
            "food": "https://food.detik.com",
            "health": "https://health.detik.com",
            "wolipop": "https://wolipop.detik.com",
            "oto": "https://oto.detik.com",
            "edu": "https://www.detik.com/edu",
        }
        self.api_endpoints = {
            "recommendation": "https://recg.detik.com/article-recommendation/wp/{user_id}?size={size}&nocache=1&ids=undefined&acctype=acc-detikcom",
            "recommendation20": "https://recg20.detik.com/article-recommendation/wp/{user_id}?size={size}",
            "terpopuler": "https://www.detik.com/terpopuler",
            "terpopuler_kanal": "https://www.detik.com/terpopuler/{days}",
        }

    def get_recommendation_articles(
        self, size=50, user_id="random.id.here"
    ) -> Dict[str, Any]:
        """
        Mengambil artikel rekomendasi dari API
        API ini memberikan artikel populer dan rekomendasi
        """
        print(f"[*] Fetching recommendation articles (size={size})...")
        url = self.api_endpoints["recommendation"].format(user_id=user_id, size=size)

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            if "body" in data and isinstance(data["body"], list):
                for item in data["body"]:
                    article = {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "url": item.get("articleurl") or item.get("desktopurl"),
                        "image": item.get("imageurl"),
                        "category": item.get("categoryauto") or item.get("programname"),
                        "type": item.get("type"),
                        "publish_date": item.get("publishdate"),
                        "description": item.get("description", ""),
                        "duration": item.get("duration"),  # untuk video
                        "video_url": item.get("videourl"),
                        "tags": (
                            item.get("tag", "").split(",") if item.get("tag") else []
                        ),
                    }
                    articles.append(article)

            print(f"[✓] Found {len(articles)} articles from recommendation API")
            return {
                "metadata": data.get("head", {}),
                "articles": articles,
                "total": len(articles),
            }
        except Exception as e:
            print(f"[!] Error fetching recommendation: {e}")
            return {"articles": [], "total": 0, "error": str(e)}

    def get_recommendation20_articles(self, size=50, user_id="test") -> Dict[str, Any]:
        """
        Mengambil artikel dari API recommendation20 (versi lain)
        """
        print(f"[*] Fetching from recg20 API (size={size})...")
        url = self.api_endpoints["recommendation20"].format(user_id=user_id, size=size)

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = []
            if "body" in data and isinstance(data["body"], list):
                for item in data["body"]:
                    article = {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "url": item.get("videourl") or item.get("articleurl"),
                        "image": item.get("imageurl") or item.get("animated"),
                        "category": item.get("programname"),
                        "type": item.get("type"),
                        "publish_date": item.get("publishdate"),
                        "description": item.get("description", ""),
                        "duration": item.get("duration"),
                        "tags": (
                            item.get("tag", "").split(",") if item.get("tag") else []
                        ),
                        "is_video": bool(item.get("videourl")),
                    }
                    articles.append(article)

            print(f"[✓] Found {len(articles)} articles from recg20 API")
            return {
                "metadata": data.get("head", {}),
                "articles": articles,
                "total": len(articles),
            }
        except Exception as e:
            print(f"[!] Error fetching recg20: {e}")
            return {"articles": [], "total": 0, "error": str(e)}

    def scrape_terpopuler(self, days=None) -> Dict[str, Any]:
        """
        Scrape halaman terpopuler untuk mendapatkan artikel trending
        days: None (all time), 1, 3, 7, 30
        """
        if days:
            url = self.api_endpoints["terpopuler_kanal"].format(days=days)
            print(f"[*] Scraping terpopuler {days} days...")
        else:
            url = self.api_endpoints["terpopuler"]
            print(f"[*] Scraping terpopuler (all time)...")

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = response.text

            # Extract article IDs dari HTML
            article_ids = re.findall(r"/d-(\d+)/", html)
            article_ids = list(set(article_ids))  # Remove duplicates

            # Extract article info dengan regex
            articles = []
            article_pattern = r'<article[^>]*>.*?href="([^"]+/d-\d+/[^"]+)"[^>]*>(.*?)</a>.*?</article>'
            matches = re.findall(article_pattern, html, re.DOTALL | re.IGNORECASE)

            for url, content in matches:
                # Extract title
                title_match = re.search(r">([^<]+)</[^>]+>$", content.strip())
                title = title_match.group(1).strip() if title_match else content.strip()
                title = re.sub(r"<[^>]+>", "", title).strip()
                title = re.sub(r"\s+", " ", title)

                # Extract ID dari URL
                id_match = re.search(r"/d-(\d+)/", url)
                article_id = id_match.group(1) if id_match else None

                if article_id:
                    articles.append(
                        {
                            "id": article_id,
                            "title": title,
                            "url": url,
                            "source": (
                                f"terpopuler_{days}" if days else "terpopuler_all"
                            ),
                        }
                    )

            print(f"[✓] Found {len(articles)} articles from terpopuler")
            return {
                "articles": articles,
                "total": len(articles),
                "unique_ids": article_ids,
            }
        except Exception as e:
            print(f"[!] Error scraping terpopuler: {e}")
            return {"articles": [], "total": 0, "error": str(e)}

    def scrape_channel_homepage(self, channel="news") -> Dict[str, Any]:
        """
        Scrape homepage dari channel tertentu (news, sport, finance, dll)
        """
        url = self.base_urls.get(channel, self.base_urls["main"])
        print(f"[*] Scraping {channel} homepage: {url}")

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            html = response.text

            # Extract semua artikel dengan berbagai pattern
            articles = []

            # Pattern 1: Standard article links
            pattern1 = r'<a[^>]*href="(https?://[^"]*\.detik\.com/[^/]+/d-(\d+)/([^"]+))"[^>]*>([^<]*)</a>'
            matches1 = re.findall(pattern1, html, re.IGNORECASE)

            for full_url, article_id, slug, title in matches1:
                title = re.sub(r"<[^>]+>", "", title).strip()
                title = re.sub(r"\s+", " ", title)
                if title and article_id:
                    articles.append(
                        {
                            "id": article_id,
                            "title": title,
                            "url": full_url,
                            "slug": slug,
                            "channel": channel,
                        }
                    )

            # Remove duplicates berdasarkan ID
            seen_ids = set()
            unique_articles = []
            for article in articles:
                if article["id"] not in seen_ids:
                    seen_ids.add(article["id"])
                    unique_articles.append(article)

            print(f"[✓] Found {len(unique_articles)} unique articles from {channel}")
            return {
                "channel": channel,
                "articles": unique_articles,
                "total": len(unique_articles),
            }
        except Exception as e:
            print(f"[!] Error scraping {channel}: {e}")
            return {"articles": [], "total": 0, "error": str(e)}

    def scrape_all_channels(self) -> Dict[str, Any]:
        """
        Scrape semua channel detik.com
        """
        print("\n[*] Scraping ALL channels...")
        all_articles = {}

        for channel_name in self.base_urls.keys():
            result = self.scrape_channel_homepage(channel_name)
            all_articles[channel_name] = result
            time.sleep(1)  # Rate limiting

        # Aggregate statistics
        total_articles = sum(channel["total"] for channel in all_articles.values())
        print(f"\n[✓] Total articles from all channels: {total_articles}")

        return all_articles

    def get_comprehensive_data(self) -> Dict[str, Any]:
        """
        Mengambil SEMUA data dari berbagai sumber
        """
        print("\n" + "=" * 60)
        print("DETIK.COM COMPREHENSIVE API SCRAPER")
        print("=" * 60 + "\n")

        all_data = {"timestamp": datetime.now().isoformat(), "sources": {}}

        # 1. Recommendation API
        print("\n### 1. RECOMMENDATION API ###")
        rec_data = self.get_recommendation_articles(size=100)
        all_data["sources"]["recommendation_api"] = rec_data
        time.sleep(1)

        # 2. Recommendation20 API (Video content)
        print("\n### 2. RECOMMENDATION20 API (Videos) ###")
        rec20_data = self.get_recommendation20_articles(size=50)
        all_data["sources"]["recommendation20_api"] = rec20_data
        time.sleep(1)

        # 3. Terpopuler All Time
        print("\n### 3. TERPOPULER (ALL TIME) ###")
        terpopuler_all = self.scrape_terpopuler()
        all_data["sources"]["terpopuler_all"] = terpopuler_all
        time.sleep(1)

        # 4. Terpopuler by timeframe
        for days in [1, 3, 7, 30]:
            print(f"\n### 4.{days}. TERPOPULER ({days} DAYS) ###")
            terpopuler = self.scrape_terpopuler(days=days)
            all_data["sources"][f"terpopuler_{days}d"] = terpopuler
            time.sleep(1)

        # 5. All Channels
        print("\n### 5. ALL CHANNELS ###")
        channels_data = self.scrape_all_channels()
        all_data["sources"]["channels"] = channels_data

        # Calculate statistics
        total_articles = 0
        unique_ids = set()

        for source_name, source_data in all_data["sources"].items():
            if source_name == "channels":
                for channel_data in source_data.values():
                    articles = channel_data.get("articles", [])
                    total_articles += len(articles)
                    for article in articles:
                        if "id" in article:
                            unique_ids.add(article["id"])
            else:
                articles = source_data.get("articles", [])
                total_articles += len(articles)
                for article in articles:
                    if "id" in article:
                        unique_ids.add(article["id"])

        all_data["statistics"] = {
            "total_articles_collected": total_articles,
            "unique_article_ids": len(unique_ids),
            "sources_count": len(all_data["sources"]),
            "channels_scraped": len(self.base_urls),
        }

        print("\n" + "=" * 60)
        print("STATISTICS")
        print("=" * 60)
        print(f"Total articles collected: {total_articles}")
        print(f"Unique article IDs: {len(unique_ids)}")
        print(f"Sources: {len(all_data['sources'])}")
        print(f"Channels scraped: {len(self.base_urls)}")
        print("=" * 60 + "\n")

        return all_data


def main():
    scraper = DetikAPIScraper()

    # Get comprehensive data
    data = scraper.get_comprehensive_data()

    # Save to JSON
    output_file = "detik_comprehensive_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[✓] Data saved to {output_file}")

    # Save unique IDs
    unique_ids = set()
    for source_name, source_data in data["sources"].items():
        if source_name == "channels":
            for channel_data in source_data.values():
                articles = channel_data.get("articles", [])
                for article in articles:
                    if "id" in article:
                        unique_ids.add(article["id"])
        else:
            articles = source_data.get("articles", [])
            for article in articles:
                if "id" in article:
                    unique_ids.add(article["id"])

    # Save IDs to text file
    ids_file = "detik_article_ids.txt"
    with open(ids_file, "w", encoding="utf-8") as f:
        for article_id in sorted(unique_ids):
            f.write(f"{article_id}\n")

    print(f"[✓] Unique IDs saved to {ids_file}")

    # Create summary report
    summary_file = "detik_scraping_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("DETIK.COM API SCRAPING SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Timestamp: {data['timestamp']}\n\n")

        f.write("STATISTICS:\n")
        f.write(
            f"  - Total articles collected: {data['statistics']['total_articles_collected']}\n"
        )
        f.write(f"  - Unique article IDs: {data['statistics']['unique_article_ids']}\n")
        f.write(f"  - Sources: {data['statistics']['sources_count']}\n")
        f.write(f"  - Channels scraped: {data['statistics']['channels_scraped']}\n\n")

        f.write("SOURCES BREAKDOWN:\n")
        for source_name, source_data in data["sources"].items():
            if source_name == "channels":
                f.write(f"\n  {source_name}:\n")
                for channel_name, channel_data in source_data.items():
                    f.write(
                        f"    - {channel_name}: {channel_data.get('total', 0)} articles\n"
                    )
            else:
                total = source_data.get("total", 0)
                f.write(f"  - {source_name}: {total} articles\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("\nAPI ENDPOINTS DISCOVERED:\n")
        f.write(
            "  - https://recg.detik.com/article-recommendation/wp/{user_id}?size={size}&nocache=1&ids=undefined&acctype=acc-detikcom\n"
        )
        f.write(
            "  - https://recg20.detik.com/article-recommendation/wp/{user_id}?size={size}\n"
        )
        f.write("  - https://www.detik.com/terpopuler\n")
        f.write("  - https://www.detik.com/terpopuler/{days}\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("\nDYNAMIC ID PATTERNS:\n")
        f.write("  - Article ID format: d-{8 digit number}\n")
        f.write("  - Example: d-8412424, d-8411977, etc.\n")
        f.write("  - Found in URLs: /{channel}/d-{id}/{slug}\n")

    print(f"[✓] Summary saved to {summary_file}")


if __name__ == "__main__":
    main()
