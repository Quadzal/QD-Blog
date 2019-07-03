from django.shortcuts import render,redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from .forms import UserChangePasswordForm, LoginForm

class Login(LoginView):
    form_class = LoginForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(Login, self).get(request, *args, **kwargs)    

class Register(CreateView):
    template_name = "user/register.html"
    form_class = UserCreationForm
    success_url = "/"
    
    def form_valid(self, form):
        super(Register, self).form_valid(form)
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
        login(self.request, user)
        return redirect("/")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(Register, self).get(request, *args, **kwargs)


class LogOut(LogoutView):
    next_page = "/"

class PasswordChange(UpdateView):
    template_name = "user/change_password.html"
    form_class = UserChangePasswordForm
    
    def get_object(self):
        return User.objects.get(username = self.request.user)
