from django.urls import path
from portal.views.home import HomePageView
from portal.views.article_detail import ArticleDetailView

app_name = "portal"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("article/<str:article_id>/", ArticleDetailView.as_view(), name="article_detail"),
]
