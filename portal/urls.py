from django.urls import path
from portal.views.home import HomePageView
from portal.views.article_detail import ArticleDetailView

app_name = "portal"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("read/<str:article_id>/", ArticleDetailView.as_view(), name="article_detail"),
    path("read/<str:article_id>/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail_slug"),
]
