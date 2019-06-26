from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import login,authenticate,logout
from article.models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data["username"]
        password = login_form.cleaned_data["password"]
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect("/")
    return render(request, "user/login.html", {"login_form":login_form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        user = register_form.save(commit=False)
        password = register_form.cleaned_data["password1"]
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username,password=password)
        login(request,user)
        return redirect("/")
    return render(request, "user/register.html", {"register_form":register_form})

@login_required(login_url="/security/login")
def logout_view(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/security/login")
def password_change_view(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            messages.success(request, 'Şifreniz Başarıyla Değiştirildi!')
            return redirect('/')
        else:
            messages.error(request, 'Lütfen Hataları Düzeltiniz.')
    
    else:
        password_change_form = PasswordChangeForm(request.user)
    
    return render(request, 'user/change_password.html', {
        'password_change_form': password_change_form
    })

