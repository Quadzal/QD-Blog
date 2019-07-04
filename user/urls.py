from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns = [
    path("login/", Login.as_view(template_name="user/login.html"), name="login"),
    path("register/", Register.as_view()),
    path("logout/", LogOut.as_view()),
    path("change/password/", PasswordChange.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)