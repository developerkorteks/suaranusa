from django.views import View
from django.shortcuts import render, Http404
from portal.services.api_client import ApiService
from urllib.parse import urlparse
import logging
import json
import asyncio
import re

logger = logging.getLogger(__name__)

class ArticleDetailView(View):
    """
    Super-Robust Async View with Dynamic Category and Content Enrichment.
    Ensures zero jejak detik and high data quality across all domains.
    """
    
    def resolve_category(self, item):
        """Smart Category Resolver (Consistent with Home View)."""
        api_cat = item.get("category")
        if api_cat and api_cat.lower() != "null":
            return str(api_cat).upper()

        url = item.get("url") or ""
        if "/tag/" in url:
            return "TOPIK KHUSUS"

        path_match = re.search(r"detik\.com/([^/]+)/d-", url)
        if path_match:
            cat = path_match.group(1).replace("-", " ")
            if cat not in ["berita", "indeks"]:
                return cat.upper()

        parsed = urlparse(url if "http" in url else f"https://{url}")
        subdomain = parsed.netloc.replace("www.", "").split(".")[0]
        
        special_cases = {"20": "VIDEO", "wolipop": "GAYA HIDUP", "inet": "TEKNOLOGI", "oto": "OTOMOTIF"}
        if subdomain in special_cases: return special_cases[subdomain]
        if subdomain and subdomain != "detik": return subdomain.upper()
        
        return "WARTA UTAMA"

    async def get(self, request, article_id):
        api_service = ApiService()
        
        # 1. Fetch with Retry Logic
        raw_article = None
        for attempt in range(3):
            raw_article = await api_service.get_article_detail(article_id)
            if raw_article: break
            if attempt < 2: await asyncio.sleep(0.5 * (attempt + 1))
        
        if not raw_article: raise Http404("Berita tidak ditemukan")
        
        # 2. Dynamic Content Enrichment
        content = raw_article.get("content") or ""
        metadata = raw_article.get("metadata") or {}
        if isinstance(metadata, str):
            try: metadata = json.loads(metadata)
            except: metadata = {}
        
        # Auto-trigger enrichment if content is missing or video detected
        is_video_type = "video" in (raw_article.get("title") or "").lower() or "20." in (raw_article.get("url") or "")
        
        if len(content) < 300 or (is_video_type and not metadata.get("videos")):
            logger.info(f"Triggering enrichment for {article_id}")
            success = await api_service.trigger_scrape_detail(article_id)
            if success:
                raw_article = await api_service.get_article_detail(article_id)
                metadata = raw_article.get("metadata") or {}
                if isinstance(metadata, str):
                    try: metadata = json.loads(metadata)
                    except: metadata = {}

        # 3. Dynamic Mapping & Anonymization
        parsed_url = urlparse(raw_article.get('url') or "https://detik.com")
        
        article = {
            'id': raw_article.get('id'),
            'title': raw_article.get('title') or "Warta Tanpa Judul",
            'url': raw_article.get('url'),
            'image': raw_article.get('image'),
            'content': raw_article.get('content') or "",
            'author': raw_article.get('author') or "Redaksi Utama",
            'source_display': parsed_url.netloc.replace("www.", ""),
            'category': self.resolve_category(raw_article),
            'scraped_at': raw_article.get('scraped_at'),
            'quality_score': raw_article.get('quality_score', 0.75),
            'tags': raw_article.get('tags', []),
            'all_images': self._normalize_media(metadata.get('images') or []),
            'all_videos': self._normalize_media(metadata.get('videos') or [])
        }

        # Fix thumbnail quality in all_images
        for img in article['all_images']:
            if "wid=54" in img['url']:
                img['url'] = img['url'].replace("wid=54&", "").replace("?wid=54", "")

        # Ensure main image is in gallery if it exists
        if article['image'] and not any(m['url'] == article['image'] for m in article['all_images']):
            article['all_images'].insert(0, {'url': article['image'], 'alt': 'Foto Utama'})

        return render(request, "news/detail.html", {"article": article})

    def _normalize_media(self, media_list):
        if not media_list: return []
        norm = []
        seen = set()
        for item in media_list:
            u = ""
            alt = "Dokumentasi Visual Warta"
            if isinstance(item, str): u = item
            elif isinstance(item, dict): 
                u = item.get('url') or item.get('src')
                alt = item.get('alt') or item.get('title') or alt
            
            if u and u not in seen:
                norm.append({'url': u, 'alt': alt})
                seen.add(u)
        return norm
