"""Modules"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
app_name = "article"
urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('about/', About.as_view(), name="about"),
    path("article/<str:slug>", ArticleView.as_view(), name="article"),
    path("author/<str:author>", AuthorView.as_view(), name="author"),
    path("search/", SearchView.as_view(), name="search"),
    path("category/<str:category>", CategoryView.as_view(), name="category"),
    path("profile/", ProfileChange.as_view(), name="profile"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
