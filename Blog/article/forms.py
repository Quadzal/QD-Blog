"""Modules"""
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Comment, UserProfile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content":forms.Textarea(attrs={"rows":10, "cols":10, "maxlength":10000})
        }
    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ["user"]

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "username":forms.TextInput(attrs={"readonly":True})
        }
        