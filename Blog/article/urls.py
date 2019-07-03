"""Modules"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns = [
    path('', Home.as_view()),
    path('about/', About.as_view()),
    path("article/<str:slug>", ArticleView.as_view()),
    path("author/<str:author>", AuthorView.as_view()),
    path("search/", SearchView.as_view()),
    path("category/<str:category>", CategoryView.as_view()),
    path("profile/", ProfileChange.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
