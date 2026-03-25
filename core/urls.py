"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from portal.views.seo import RobotsTxtView, SitemapXmlView, LatestNewsFeedView, ServiceWorkerView, ManifestJsonView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", RobotsTxtView.as_view(), name="robots_txt"),
    path("sitemap.xml", SitemapXmlView.as_view(), name="sitemap_xml"),
    path("feed/", LatestNewsFeedView.as_view(), name="news_feed"),
    path("sw.js", ServiceWorkerView.as_view(), name="service_worker"),
    path("manifest.json", ManifestJsonView.as_view(), name="manifest_json"),
    path("", include("portal.urls", namespace="portal")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
