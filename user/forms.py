from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from article.models import UserProfile
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20,widget=forms.TextInput, label="Kullanıcı Adı", min_length=8)
    password = forms.CharField(max_length=32, min_length=8, label="Şifre", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("Kullanıcı Adını Veya Parolayı Yanlış Girdiniz.")
        return super(LoginForm, self).clean()


class RegisterForm(forms.ModelForm):
    
    username = forms.CharField(max_length=20, label="Kullanıcı Adı", min_length=8)
    password1 = forms.CharField(max_length=32, min_length=8, label="Şifre", widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, min_length=8, label="Şifreyi Doğrulayınız", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2"
        ]

    def clean(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if (password1 and password2) and password1 != password2:
            raise forms.ValidationError("Şifreler Eşleşmiyor!")
        super(RegisterForm, self).clean() 
