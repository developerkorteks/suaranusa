import httpx
from django.conf import settings
from urllib.parse import urlparse
import re

from portal.models import AdSlot
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

from django.core.cache import cache

def advertisements(request):
    """
    Context processor to provide active advertisement scripts and URLs.
    Reads from CACHE to avoid SynchronousOnlyOperation in async views.
    """
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile = any(x in ua for x in ['iphone', 'android', 'mobile', 'ipod', 'opera mini', 'blackberry'])
    
    # We use a combined cache key to simplify
    cached_ads = cache.get('active_ad_slots_data')
    
    # If cache is missing, return empty but don't try to query DB here
    # Querying DB in a context processor triggered by an async view is unstable.
    if not cached_ads:
        return {"ads": {"CACHE_MISS": "Run populate_ad_cache"}, "ads_urls": {}}

    ads_data = {}
    ads_urls = {}
    
    for slot in cached_ads:
        slug = slot['slug']
        # Determine script
        script = slot['m_script'] if (is_mobile and slot['m_script']) else slot['d_script']
        if not script: script = slot['d_script'] or slot['m_script']
        
        if script:
            ads_data[slug] = script
        if slot['d_url']:
            ads_urls[slug] = slot['d_url']

    return {
        "ads": ads_data,
        "ads_urls": ads_urls
    }

def dynamic_categories(request):
    """
    Context processor to provide ALL dynamic categories to templates.
    """
    try:
        # Fetch a larger sample to ensure we get all categories
        response = httpx.post(f"{settings.API_BASE_URL}/api/articles/search", json={"limit": 250}, timeout=3.0)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            categories = set()
            
            for item in articles:
                api_cat = item.get("category")
                if api_cat and api_cat.lower() != "null":
                    categories.add(str(api_cat).upper())
                    continue

                url = item.get("url") or ""
                if "/tag/" in url:
                    categories.add("TOPIK KHUSUS")
                    continue
                
                path_match = re.search(r"detik\.com/([^/]+)/d-", url)
                if path_match:
                    cat = path_match.group(1).replace("-", " ")
                    if cat not in ["berita", "indeks"]:
                        categories.add(cat.upper())
                        continue

                parsed = urlparse(url if "http" in url else f"https://{url}")
                subdomain = parsed.netloc.replace("www.", "").split(".")[0]
                
                special_cases = {"20": "VIDEO", "wolipop": "GAYA HIDUP", "inet": "TEKNOLOGI", "oto": "OTOMOTIF"}
                if subdomain in special_cases:
                    categories.add(special_cases[subdomain])
                elif subdomain and subdomain != "detik":
                    categories.add(subdomain.upper())
            
            sorted_cats = sorted(list(categories))
            return {
                "nav_categories_main": sorted_cats[:5],  # First 5 for main bar
                "nav_categories_more": sorted_cats[5:],  # The rest for dropdown
                "nav_categories_all": sorted_cats,       # All for mobile menu
                "category_count": len(sorted_cats)
            }
    except Exception:
        pass
    
    fallback = ["NASIONAL", "EKONOMI", "INTERNASIONAL", "TEKNOLOGI", "HIBURAN", "OLAHRAGA", "GAYA HIDUP"]
    return {
        "nav_categories_main": fallback[:5],
        "nav_categories_more": fallback[5:],
        "nav_categories_all": fallback,
        "category_count": len(fallback)
    }
