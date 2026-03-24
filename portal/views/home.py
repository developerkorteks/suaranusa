from django.views import View
from django.shortcuts import render
from portal.services.api_client import ApiService
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
    """
    
    def resolve_category(self, item):
        """Smartly resolves category from URL and source without hardcoding."""
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
        
        # 1. Fetch articles from API
        raw_articles = await api_service.get_articles(limit=1000, query=search_query)
        
        processed_articles = []
        all_categories = set()

        for item in raw_articles:
            clean_category = self.resolve_category(item)
            all_categories.add(clean_category)
            
            url = item.get("url") or ""
            title = item.get("title") or ""
            parsed_url = urlparse(url if "http" in url else f"https://{url}")
            source_display = parsed_url.netloc.replace("www.", "") or "detik.com"
            
            metadata = item.get("metadata") or {}
            if isinstance(metadata, str):
                try: metadata = json.loads(metadata)
                except: metadata = {}
            
            # --- ROBUST VIDEO DETECTION (Smart Mapping) ---
            # Indikator video: 
            # 1. Domain 20.detik.com
            # 2. String "video" di URL path
            # 3. String "video" di Judul
            # 4. Ada list 'videos' di metadata
            is_video = (
                "20.detik.com" in source_display or 
                "/video-" in url.lower() or 
                "video:" in title.lower() or 
                bool(metadata.get("videos"))
            )
            
            article_obj = {
                'id': item.get('id'),
                'title': title or "Berita Terkini",
                'image': item.get("image") or (metadata.get("images")[0].get("url") if metadata.get("images") else None),
                'category': clean_category,
                'author': item.get('author') or "Redaksi",
                'date': (item.get('publish_date') or item.get('scraped_at') or "2026-03-24")[:10],
                'is_video': is_video,
                'is_gallery': bool(metadata.get("images") and len(metadata.get("images")) > 1),
                'is_long_read': len(item.get("content") or "") > 2500,
                'quality_score': item.get('quality_score', 0.5),
                'source_display': source_display
            }

            # Filter logic
            if selected_category:
                if article_obj['category'].upper() == selected_category.upper():
                    processed_articles.append(article_obj)
            else:
                processed_articles.append(article_obj)

        unique_categories = sorted(list(all_categories))

        context = {
            "articles": processed_articles,
            "total_count": len(processed_articles),
            "category_count": len(unique_categories),
            "categories": unique_categories,
            "selected_category": selected_category,
            "search_query": search_query
        }
        
        return render(request, "news/home.html", context)
