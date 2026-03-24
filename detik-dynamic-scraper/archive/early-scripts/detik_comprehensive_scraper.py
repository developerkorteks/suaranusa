#!/usr/bin/env python3
"""
Detik.com Comprehensive Multi-Channel Scraper
Mengambil data dari SEMUA subdomain dan endpoint API yang ditemukan
Based on analysis from detailcyberlife.md
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys


class DetikComprehensiveScraper:
    """Scraper untuk semua channel dan subdomain detik.com"""

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
            "Referer": "https://www.detik.com/",
            "Origin": "https://www.detik.com",
        }

        # Subdomain yang ditemukan (32 subdomain)
        self.subdomains = {
            "main": "https://www.detik.com",
            "20": "https://20.detik.com",
            "news": "https://news.detik.com",
            "finance": "https://finance.detik.com",
            "sport": "https://sport.detik.com",
            "hot": "https://hot.detik.com",
            "inet": "https://inet.detik.com",
            "travel": "https://travel.detik.com",
            "food": "https://food.detik.com",
            "health": "https://health.detik.com",
            "oto": "https://oto.detik.com",
            "wolipop": "https://wolipop.detik.com",
            "foto": "https://foto.detik.com",
            "event": "https://event.detik.com",
            "karir": "https://karir.detik.com",
            # API Subdomains
            "rech": "https://rech.detik.com",
            "rech20": "https://rech20.detik.com",
            "recg": "https://recg.detik.com",
            "rekomendit": "https://rekomendit.detik.com",
            "apicomment": "https://apicomment.detik.com",
            "connect": "https://connect.detik.com",
            "explore-api": "https://explore-api.detik.com",
            # Media/CDN
            "cdnv": "https://cdnv.detik.com",
            "cdnstatic": "https://cdnstatic.detik.com",
            "vod": "https://vod.detik.com",
            # Other services
            "adsmart": "https://adsmart.detik.com",
            "analytic": "https://analytic.detik.com",
            "collent": "https://collent.detik.com",
            "fyb": "https://fyb.detik.com",
            "kemiri": "https://kemiri.detik.com",
            "newrevive": "https://newrevive.detik.com",
            "pasangmata": "https://pasangmata.detik.com",
        }

        # Channel mapping dengan acctype
        self.channels = {
            "news": "acc-detiknews",
            "finance": "acc-detikfinance",
            "sport": "acc-detiksport",
            "hot": "acc-detikhot",
            "inet": "acc-detikinet",
            "travel": "acc-detiktravel",
            "food": "acc-detikfood",
            "health": "acc-detikhealth",
            "oto": "acc-detikoto",
            "main": "acc-detikcom",
        }

        # API Endpoints yang ditemukan
        self.api_endpoints = {
            "rech_detail": "https://rech.detik.com/article-recommendation/detail/{user_id}?size={size}&nocache=1&ids={ids}&acctype={acctype}",
            "rech_wp": "https://rech.detik.com/article-recommendation/wp/{user_id}?size={size}&nocache=1&ids={ids}&acctype={acctype}",
            "rech20_detail": "https://rech20.detik.com/article-recommendation/detail/{user_id}",
            "recg_detail": "https://recg.detik.com/article-recommendation/detail/{user_id}?size={size}&nocache=1&ids={ids}&acctype={acctype}",
            "recg_wp": "https://recg.detik.com/article-recommendation/wp/{user_id}?size={size}&nocache=1&ids={ids}&acctype={acctype}",
            "recg_sticky": "https://recg.detik.com/article-recommendation/sticky/{user_id}?size={size}&nocache=1&ids={ids}&acctype={acctype}",
            "recg_index": "https://recg.detik.com/article-recommendation/index/{user_id}?size={size}&nocache=1&ids={ids}&acctype={acctype}",
        }

        self.user_id = "comprehensive.scraper.2026"

    def _fetch_json(self, url: str, referer: str = None) -> Dict:
        """Fetch JSON dari URL"""
        try:
            headers = self.headers.copy()
            if referer:
                headers["Referer"] = referer
                headers["Origin"] = referer.split("/")[0] + "//" + referer.split("/")[2]

            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            print(f"  ✗ HTTP Error {e.code}: {url}")
            return None
        except urllib.error.URLError as e:
            print(f"  ✗ URL Error: {e.reason}")
            return None
        except json.JSONDecodeError as e:
            print(f"  ✗ JSON Error: {e}")
            return None
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return None

    def get_channel_recommendations_rech(
        self, channel: str, size: int = 20, endpoint_type: str = "detail"
    ) -> Dict:
        """
        Ambil rekomendasi artikel dari channel tertentu menggunakan rech.detik.com
        endpoint_type: 'detail' atau 'wp'
        """
        acctype = self.channels.get(channel, "acc-detikcom")

        if endpoint_type == "detail":
            url = self.api_endpoints["rech_detail"].format(
                user_id=self.user_id, size=size, ids="undefined", acctype=acctype
            )
        else:  # wp
            url = self.api_endpoints["rech_wp"].format(
                user_id=self.user_id, size=size, ids="undefined", acctype=acctype
            )

        referer = self.subdomains.get(channel, "https://www.detik.com")

        print(f"  Fetching {channel} ({endpoint_type}): {size} items...")
        data = self._fetch_json(url, referer)

        if data and "body" in data:
            articles = []
            for item in data["body"]:
                article = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "url": item.get("articleurl") or item.get("desktopurl"),
                    "image": item.get("imageurl"),
                    "category": item.get("categoryauto"),
                    "publish_date": item.get("publishdate"),
                    "description": item.get("resume", ""),
                    "tags": item.get("tag", "").split("|") if item.get("tag") else [],
                    "author": item.get("penulis", ""),
                    "channel": channel,
                    "source_api": f"rech_{endpoint_type}",
                }
                articles.append(article)

            print(f"  ✓ Got {len(articles)} articles from {channel} ({endpoint_type})")
            return {
                "channel": channel,
                "endpoint": endpoint_type,
                "articles": articles,
                "metadata": data.get("head", {}),
                "total": len(articles),
            }

        return {"channel": channel, "articles": [], "total": 0, "error": "No data"}

    def get_channel_recommendations_recg(
        self, channel: str, size: int = 20, endpoint_type: str = "wp"
    ) -> Dict:
        """
        Ambil rekomendasi artikel dari channel tertentu menggunakan recg.detik.com
        endpoint_type: 'detail', 'wp', 'sticky', 'index'
        """
        acctype = self.channels.get(channel, "acc-detikcom")

        endpoint_key = f"recg_{endpoint_type}"
        if endpoint_key not in self.api_endpoints:
            return {
                "channel": channel,
                "articles": [],
                "total": 0,
                "error": f"Invalid endpoint type: {endpoint_type}",
            }

        url = self.api_endpoints[endpoint_key].format(
            user_id=self.user_id, size=size, ids="undefined", acctype=acctype
        )

        referer = self.subdomains.get(channel, "https://www.detik.com")

        print(f"  Fetching {channel} from recg ({endpoint_type}): {size} items...")
        data = self._fetch_json(url, referer)

        if data and "body" in data:
            articles = []
            for item in data["body"]:
                article = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "url": item.get("articleurl") or item.get("desktopurl"),
                    "image": item.get("imageurl"),
                    "category": item.get("categoryauto"),
                    "publish_date": item.get("publishdate"),
                    "description": item.get("resume", ""),
                    "tags": item.get("tag", "").split("|") if item.get("tag") else [],
                    "channel": channel,
                    "source_api": f"recg_{endpoint_type}",
                }
                articles.append(article)

            print(
                f"  ✓ Got {len(articles)} articles from {channel} (recg_{endpoint_type})"
            )
            return {
                "channel": channel,
                "endpoint": f"recg_{endpoint_type}",
                "articles": articles,
                "metadata": data.get("head", {}),
                "total": len(articles),
            }

        return {"channel": channel, "articles": [], "total": 0, "error": "No data"}

    def get_video_recommendations(self, size: int = 30) -> Dict:
        """Ambil rekomendasi video dari rech20.detik.com"""
        url = self.api_endpoints["rech20_detail"].format(user_id=self.user_id)

        print(f"  Fetching videos from rech20: {size} items...")

        # rech20 needs Content-Type: application/json
        headers = self.headers.copy()
        headers["Content-Type"] = "application/json"
        headers["Referer"] = "https://20.detik.com/"
        headers["Origin"] = "https://20.detik.com"

        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode("utf-8"))

                if data and "body" in data:
                    videos = []
                    for item in data["body"][:size]:
                        video = {
                            "id": item.get("id"),
                            "title": item.get("title"),
                            "url": item.get("videourl") or item.get("articleurl"),
                            "image": item.get("imageurl") or item.get("animated"),
                            "animated_preview": item.get("animated"),
                            "duration": item.get("duration"),
                            "program": item.get("programname"),
                            "publish_date": item.get("publishdate"),
                            "description": item.get("description", ""),
                            "tags": (
                                item.get("tag", "").split(",")
                                if item.get("tag")
                                else []
                            ),
                            "smil": item.get("smil"),
                            "is_vertical": item.get("is_vertical_video") == "1",
                            "source_api": "rech20_detail",
                        }
                        videos.append(video)

                    print(f"  ✓ Got {len(videos)} videos from rech20")
                    return {
                        "videos": videos,
                        "metadata": data.get("head", {}),
                        "total": len(videos),
                    }
        except Exception as e:
            print(f"  ✗ Error fetching videos: {e}")

        return {"videos": [], "total": 0, "error": "Failed to fetch"}

    def scrape_all_channels_comprehensive(self, articles_per_channel: int = 30) -> Dict:
        """
        Scrape SEMUA channel menggunakan SEMUA endpoint yang tersedia
        """
        print("\n" + "=" * 80)
        print("DETIK.COM COMPREHENSIVE MULTI-CHANNEL SCRAPER")
        print("=" * 80)
        print(f"\nTotal Subdomains: {len(self.subdomains)}")
        print(f"Total Channels with API: {len(self.channels)}")
        print(f"Total API Endpoints: {len(self.api_endpoints)}")
        print("\n" + "=" * 80 + "\n")

        all_data = {
            "timestamp": datetime.now().isoformat(),
            "scraper_info": {
                "total_subdomains": len(self.subdomains),
                "total_channels": len(self.channels),
                "total_api_endpoints": len(self.api_endpoints),
                "articles_per_channel": articles_per_channel,
            },
            "channels": {},
            "videos": {},
            "statistics": {},
        }

        # 1. Scrape semua channel dengan rech.detik.com (detail)
        print("### PHASE 1: RECH.DETIK.COM (DETAIL) ###\n")
        for channel in self.channels.keys():
            try:
                result = self.get_channel_recommendations_rech(
                    channel, articles_per_channel, "detail"
                )
                if channel not in all_data["channels"]:
                    all_data["channels"][channel] = {}
                all_data["channels"][channel]["rech_detail"] = result
                time.sleep(0.5)
            except Exception as e:
                print(f"  ✗ Error scraping {channel} (rech_detail): {e}")

        # 2. Scrape semua channel dengan rech.detik.com (wp)
        print("\n### PHASE 2: RECH.DETIK.COM (WP) ###\n")
        for channel in self.channels.keys():
            try:
                result = self.get_channel_recommendations_rech(
                    channel, articles_per_channel, "wp"
                )
                all_data["channels"][channel]["rech_wp"] = result
                time.sleep(0.5)
            except Exception as e:
                print(f"  ✗ Error scraping {channel} (rech_wp): {e}")

        # 3. Scrape semua channel dengan recg.detik.com (wp)
        print("\n### PHASE 3: RECG.DETIK.COM (WP) ###\n")
        for channel in self.channels.keys():
            try:
                result = self.get_channel_recommendations_recg(
                    channel, articles_per_channel, "wp"
                )
                all_data["channels"][channel]["recg_wp"] = result
                time.sleep(0.5)
            except Exception as e:
                print(f"  ✗ Error scraping {channel} (recg_wp): {e}")

        # 4. Scrape videos dari rech20.detik.com
        print("\n### PHASE 4: RECH20.DETIK.COM (VIDEOS) ###\n")
        try:
            videos_result = self.get_video_recommendations(50)
            all_data["videos"] = videos_result
        except Exception as e:
            print(f"  ✗ Error fetching videos: {e}")

        # 5. Calculate statistics
        print("\n### CALCULATING STATISTICS ###\n")

        total_articles = 0
        unique_ids = set()
        articles_by_channel = {}

        for channel, endpoints in all_data["channels"].items():
            channel_total = 0
            for endpoint, data in endpoints.items():
                articles = data.get("articles", [])
                channel_total += len(articles)
                total_articles += len(articles)

                for article in articles:
                    if article.get("id"):
                        unique_ids.add(article["id"])

            articles_by_channel[channel] = channel_total

        # Add video IDs
        for video in all_data["videos"].get("videos", []):
            if video.get("id"):
                unique_ids.add(video["id"])

        total_videos = len(all_data["videos"].get("videos", []))

        all_data["statistics"] = {
            "total_articles": total_articles,
            "total_videos": total_videos,
            "total_content": total_articles + total_videos,
            "unique_ids": len(unique_ids),
            "articles_by_channel": articles_by_channel,
            "channels_scraped": len(self.channels),
            "endpoints_used": len(self.api_endpoints),
        }

        print("=" * 80)
        print("SCRAPING COMPLETE")
        print("=" * 80)
        print(f"Total Articles: {total_articles}")
        print(f"Total Videos: {total_videos}")
        print(f"Total Content: {total_articles + total_videos}")
        print(f"Unique IDs: {len(unique_ids)}")
        print(f"Channels: {len(self.channels)}")
        print("\nArticles by Channel:")
        for channel, count in sorted(
            articles_by_channel.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {channel:12s}: {count:4d} articles")
        print("=" * 80 + "\n")

        return all_data


def main():
    """Main function"""
    scraper = DetikComprehensiveScraper()

    # Scrape all channels
    data = scraper.scrape_all_channels_comprehensive(articles_per_channel=30)

    # Save comprehensive data
    output_file = "detik_all_channels_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[✓] Comprehensive data saved to: {output_file}")

    # Save unique IDs
    unique_ids = set()
    for channel, endpoints in data["channels"].items():
        for endpoint, endpoint_data in endpoints.items():
            for article in endpoint_data.get("articles", []):
                if article.get("id"):
                    unique_ids.add(article["id"])

    for video in data["videos"].get("videos", []):
        if video.get("id"):
            unique_ids.add(video["id"])

    ids_file = "detik_all_unique_ids.txt"
    with open(ids_file, "w", encoding="utf-8") as f:
        for uid in sorted(unique_ids):
            f.write(f"{uid}\n")
    print(f"[✓] Unique IDs saved to: {ids_file}")

    # Create comprehensive summary
    summary_file = "detik_comprehensive_summary.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("DETIK.COM COMPREHENSIVE SCRAPING SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Timestamp: {data['timestamp']}\n\n")

        f.write("SCRAPER INFO:\n")
        f.write(f"  Total Subdomains: {data['scraper_info']['total_subdomains']}\n")
        f.write(f"  Total Channels: {data['scraper_info']['total_channels']}\n")
        f.write(
            f"  Total API Endpoints: {data['scraper_info']['total_api_endpoints']}\n"
        )
        f.write(
            f"  Articles per Channel: {data['scraper_info']['articles_per_channel']}\n\n"
        )

        f.write("STATISTICS:\n")
        f.write(f"  Total Articles: {data['statistics']['total_articles']}\n")
        f.write(f"  Total Videos: {data['statistics']['total_videos']}\n")
        f.write(f"  Total Content: {data['statistics']['total_content']}\n")
        f.write(f"  Unique IDs: {data['statistics']['unique_ids']}\n\n")

        f.write("ARTICLES BY CHANNEL:\n")
        for channel, count in sorted(
            data["statistics"]["articles_by_channel"].items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            f.write(f"  {channel:12s}: {count:4d} articles\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("\nALL SUBDOMAINS FOUND (32 total):\n")
        for name, url in sorted(scraper.subdomains.items()):
            f.write(f"  {name:15s}: {url}\n")

        f.write("\n" + "=" * 80 + "\n")
        f.write("\nALL API ENDPOINTS (7 total):\n")
        for name, template in sorted(scraper.api_endpoints.items()):
            f.write(f"  {name}:\n")
            f.write(f"    {template}\n\n")

        f.write("=" * 80 + "\n")

    print(f"[✓] Summary saved to: {summary_file}")

    print("\n" + "=" * 80)
    print("ALL FILES GENERATED")
    print("=" * 80)
    print(f"1. {output_file} - Complete JSON data")
    print(f"2. {ids_file} - All unique IDs")
    print(f"3. {summary_file} - Text summary")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
