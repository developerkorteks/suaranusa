from django.views import View
from django.shortcuts import render
from django.utils.text import slugify
from portal.services.api_client import ApiService
from portal.models import ManualArticle
from asgiref.sync import sync_to_async
from urllib.parse import urlparse
import logging
import json
import re

logger = logging.getLogger(__name__)

class HomePageView(View):
    """
    Enhanced Dynamic View:
    - Smart dynamic mapping based on URL patterns, subdomains, and media types.
    - Robust Video detection for cross-domain content.
    - NEW: Merges manual articles from local DB with Scraper API data.
    """
    
    def resolve_category(self, item):
        """Smartly resolves category from URL and source without hardcoding."""
        # For manual articles, use the category field directly
        if item.get('is_manual'):
            return str(item.get("category")).upper()

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

    async def get(self, request):
        api_service = ApiService()
        selected_category = request.GET.get('cat')
        search_query = request.GET.get('q')
        
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
            
        page_size = 12
        
        # 1. Fetch from Local DB (Manual Articles)
        # We fetch manual articles that match search query or category
        def get_manual_articles_sync():
            qs = ManualArticle.objects.filter(is_published=True)
            if selected_category:
                qs = qs.filter(category__iexact=selected_category)
            if search_query:
                qs = qs.filter(title__icontains=search_query) | qs.filter(content__icontains=search_query)
            # Fetch a buffer to allow meaningful merging
            return [obj.to_dict() for obj in qs[:50]]

        manual_raw = await sync_to_async(get_manual_articles_sync)()

        # 2. Fetch from Scraper API
        # We fetch a buffer from API as well
        fetch_limit = 50 
        raw_api_articles = await api_service.get_articles(
            limit=fetch_limit, 
            offset=(page - 1) * page_size, 
            query=search_query,
            category=selected_category
        )
        
        # Combine Raw Data
        all_raw = manual_raw + raw_api_articles
        
        processed_articles = []

        for item in all_raw:
            clean_category = self.resolve_category(item)
            
            url = item.get("url") or ""
            title = item.get("title") or ""
            parsed_url = urlparse(url if "http" in url else f"https://{url}")
            source_display = parsed_url.netloc.replace("www.", "") or "detik.com"
            
            metadata = item.get("metadata") or {}
            if isinstance(metadata, str):
                try: metadata = json.loads(metadata)
                except: metadata = {}
            
            is_video = ("20.detik.com" in source_display or "/video-" in url.lower() or bool(metadata.get("videos")))
            
            # Use publish_date or scraped_at for sorting
            sort_date = item.get('publish_date') or item.get('scraped_at') or "2026-03-24"
            
            article_obj = {
                'id': item.get('id'),
                'title': title or "Berita Terkini",
                'slug': slugify(title or "berita-terkini"),
                'image': item.get("image") or (metadata.get("images")[0].get("url") if metadata.get("images") else None),
                'category': clean_category,
                'author': item.get('author') or "Redaksi",
                'date': sort_date[:10],
                'sort_date': sort_date, # Internal use for sorting
                'is_video': is_video,
                'is_gallery': bool(metadata.get("images") and len(metadata.get("images")) > 1),
                'is_long_read': len(item.get("content") or "") > 2500,
                'quality_score': item.get('quality_score', 0.5),
                'source_display': source_display,
                'is_manual': item.get('is_manual', False)
            }

            processed_articles.append(article_obj)

        # 3. Sort Combined Articles by sort_date DESC
        processed_articles.sort(key=lambda x: x['sort_date'], reverse=True)

        # 4. Final Pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paged_articles = processed_articles[start_idx:end_idx]
        
        has_next = len(processed_articles) > end_idx

        context = {
            "articles": paged_articles,
            "total_count": len(processed_articles),
            "selected_category": selected_category,
            "search_query": search_query,
            "page": page,
            "has_next": has_next,
            "has_prev": page > 1,
            "next_page": page + 1,
            "prev_page": page - 1
        }
        
        return render(request, "news/home.html", context)
