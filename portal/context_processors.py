import httpx
from django.conf import settings
from urllib.parse import urlparse
import re

from portal.models import AdSlot
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def advertisements(request):
    """
    Context processor to provide active advertisement scripts and URLs to all templates.
    """
    ads_data = {}
    ads_urls = {}
    
    # Identify device type
    ua = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile = any(x in ua for x in ['iphone', 'android', 'mobile', 'ipod', 'opera mini', 'blackberry'])
    
    cache_key = 'active_ad_slots_mobile' if is_mobile else 'active_ad_slots_desktop'
    cached_payload = cache.get(cache_key)

    if cached_payload is None:
        ads_data = {}
        ads_urls = {}
        try:
            active_slots = AdSlot.objects.filter(is_active=True)
            for slot in active_slots:
                # Handle Scripts
                if is_mobile:
                    ads_data[slot.position_slug] = slot.mobile_script or slot.desktop_script
                else:
                    ads_data[slot.position_slug] = slot.desktop_script or slot.mobile_script
                
                # Handle Direct URLs (Smartlinks)
                if slot.direct_url:
                    ads_urls[slot.position_slug] = slot.direct_url
            
            # Cache the combined data
            payload = {"scripts": ads_data, "urls": ads_urls}
            cache.set(cache_key, payload, 3600)
            cached_payload = payload
        except:
            return {"ads": {}, "ads_urls": {}}

    return {
        "ads": cached_payload.get("scripts", {}),
        "ads_urls": cached_payload.get("urls", {})
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
                "nav_categories_all": sorted_cats        # All for mobile menu
            }
    except Exception:
        pass
    
    fallback = ["NASIONAL", "EKONOMI", "INTERNASIONAL", "TEKNOLOGI", "HIBURAN", "OLAHRAGA", "GAYA HIDUP"]
    return {
        "nav_categories_main": fallback[:5],
        "nav_categories_more": fallback[5:],
        "nav_categories_all": fallback
    }
