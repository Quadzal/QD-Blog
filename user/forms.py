from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from article.models import UserProfile
from django.contrib.auth.forms import (
    UserCreationForm, 
    PasswordChangeForm,
    AuthenticationForm)


class UserChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(max_length=32,
        min_length=8,
        label="Eski Parola",
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        max_length=32, 
        min_length=8, 
        label="Yeni Parola", 
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(max_length=32,
        min_length=8, 
        label="Yeni Parolayı Doğrula", 
        widget=forms.PasswordInput()
    )
    class Meta:
        model = User
        fields = []

    def save(self, commit=False):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["new_password"])
        instance.save()
