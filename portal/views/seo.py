from django.http import HttpResponse
from django.views import View
from portal.services.api_client import ApiService
from django.utils.text import slugify
import datetime

class RobotsTxtView(View):
    def get(self, request):
        lines = [
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")

class SitemapXmlView(View):
    async def get(self, request):
        api_service = ApiService()
        # Fetch 50 latest articles for the sitemap
        articles = await api_service.get_articles(limit=50)
        
        base_url = f"{request.scheme}://{request.get_host()}"
        
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        # Add Homepage
        xml_content.append(f'  <url><loc>{base_url}/</loc><priority>1.0</priority></url>')
        
        # Add Articles
        for article in articles:
            article_id = article.get('id')
            title = article.get('title') or "news"
            slug = slugify(title)
            # Use the new slugged URL pattern
            url = f"{base_url}/read/{article_id}/{slug}/"
            xml_content.append(f'  <url><loc>{url}</loc><priority>0.8</priority></url>')
            
        xml_content.append('</urlset>')
        
        return HttpResponse("\n".join(xml_content), content_type="application/xml")

class LatestNewsFeedView(View):
    async def get(self, request):
        api_service = ApiService()
        # Fetch 30 latest articles for the feed
        articles = await api_service.get_articles(limit=30)
        
        base_url = f"{request.scheme}://{request.get_host()}"
        now = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0700")
        
        xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_content.append('<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">')
        xml_content.append('  <channel>')
        xml_content.append('    <title>suaranusa | Premium Editorial</title>')
        xml_content.append(f'    <link>{base_url}/</link>')
        xml_content.append('    <description>Portal berita premium suaranusa menyajikan jurnalisme mendalam dan terpercaya.</description>')
        xml_content.append(f'    <lastBuildDate>{now}</lastBuildDate>')
        xml_content.append('    <language>id-id</language>')
        
        for article in articles:
            article_id = article.get('id')
            title = article.get('title') or "Berita Terkini"
            slug = slugify(title)
            url = f"{base_url}/read/{article_id}/{slug}/"
            
            # Simple content cleaning for RSS
            content = article.get('content') or ""
            description = (content[:300] + '...') if len(content) > 300 else content
            
            xml_content.append('    <item>')
            xml_content.append(f'      <title>{title}</title>')
            xml_content.append(f'      <link>{url}</link>')
            xml_content.append(f'      <guid isPermaLink="false">{article_id}</guid>')
            xml_content.append(f'      <description><![CDATA[{description}]]></description>')
            xml_content.append(f'      <dc:creator>{article.get("author") or "Redaksi suaranusa"}</dc:creator>')
            xml_content.append(f'      <pubDate>{now}</pubDate>') # Approximation as we don't have full TZ pubDate
            xml_content.append('    </item>')
            
        xml_content.append('  </channel>')
        xml_content.append('</rss>')
        
        return HttpResponse("\n".join(xml_content), content_type="application/rss+xml")

class ServiceWorkerView(View):
    def get(self, request):
        # Service workers must be served from the root to have full scope
        try:
            with open('static/sw.js', 'rb') as f:
                return HttpResponse(f.read(), content_type="application/javascript")
        except FileNotFoundError:
            return HttpResponse("// sw.js not found", content_type="application/javascript")

class ManifestJsonView(View):
    def get(self, request):
        try:
            with open('static/manifest.json', 'rb') as f:
                return HttpResponse(f.read(), content_type="application/json")
        except FileNotFoundError:
            return HttpResponse('{"name": "suaranusa"}', content_type="application/json")
