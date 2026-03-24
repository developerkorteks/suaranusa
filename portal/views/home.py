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
        
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
            
        page_size = 12
        
        # 1. Fetch a larger chunk from API to allow local filtering
        # Since many database category fields are null, we filter via resolve_category
        # If searching, we hit the API hard. If filtering category, we fetch more.
        fetch_limit = 100 if selected_category else page_size + 1
        raw_articles = await api_service.get_articles(
            limit=fetch_limit, 
            offset=0 if selected_category else (page - 1) * page_size, 
            query=search_query
        )
        
        processed_articles = []
        all_categories = set(["NASIONAL", "EKONOMI", "INTERNASIONAL", "TEKNOLOGI", "HIBURAN", "OLAHRAGA", "GAYA HIDUP"])

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
            
            is_video = ("20.detik.com" in source_display or "/video-" in url.lower() or bool(metadata.get("videos")))
            
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

            # Filter logic (Local)
            if selected_category:
                if article_obj['category'].upper() == selected_category.upper():
                    processed_articles.append(article_obj)
            else:
                processed_articles.append(article_obj)

        # Slice for pagination
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paged_articles = processed_articles[start_idx:end_idx] if selected_category else processed_articles[:page_size]
        
        has_next = len(processed_articles) > end_idx if selected_category else len(raw_articles) > page_size
        unique_categories = sorted(list(all_categories))

        context = {
            "articles": paged_articles,
            "total_count": len(processed_articles),
            "category_count": len(unique_categories),
            "categories": unique_categories,
            "selected_category": selected_category,
            "search_query": search_query,
            "page": page,
            "has_next": has_next,
            "has_prev": page > 1,
            "next_page": page + 1,
            "prev_page": page - 1
        }
        
        return render(request, "news/home.html", context)
