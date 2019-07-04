from django.shortcuts import render,redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserChangePasswordForm

class Login(LoginView):
    success_url = reverse_lazy("article:home")
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super(Login, self).get(request, *args, **kwargs)    


class Register(CreateView):
    template_name = "user/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("article:home")
    
    def form_valid(self, form):
        super(Register, self).form_valid(form)
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password1"])
        login(self.request, user)
        return redirect("article:home")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("article:home")
        return super(Register, self).get(request, *args, **kwargs)



class LogOut(LogoutView):
    next_page = reverse_lazy("article:home")


class PasswordChange(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    template_name = "user/change_password.html"
    form_class = UserChangePasswordForm
    
    def get_object(self):
        return User.objects.get(username=self.request.user)
