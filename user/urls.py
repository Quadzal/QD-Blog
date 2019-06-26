from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('login/', login_view),
    path('register/', register_view),
    path("logout/", logout_view),
    path("change/password/", password_change_view)
]