from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='cloudflare_safe')
def cloudflare_safe(script_code):
    """
    Injects data-cfasync="false" into script tags to prevent 
    Cloudflare RocketLoader from breaking Adsterra ads.
    """
    if not script_code:
        return ""
    
    # Pattern to find <script type=... or <script src=...
    # We insert data-cfasync="false" right after '<script'
    fixed_code = re.sub(r'<script', '<script data-cfasync="false"', script_code, flags=re.IGNORECASE)
    
    return mark_safe(fixed_code)
