"""Modules"""
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import UpdateView, ListView, CreateView, TemplateView
from .models import Article, Category, UserProfile
from .forms import CommentForm, UserProfileForm, CustomUserChangeForm

def handler404(request, exception):
    return render(request, "shared/404.html")

def getCategoryList():
    """
        Kategorileri Veritabanından Çeker.
    """
    categoryList = Category.objects.all()
    return categoryList

class Home(ListView):
    template_name = "article/index.html"
    queryset = Article.objects.all()
    paginate_by = 10
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = getCategoryList()
        return context

class About(TemplateView):
    template_name = "article/about.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = getCategoryList()
        return context

class AuthorView(ListView):
    template_name = "article/index.html"
    paginate_by = 10
    context_object_name = "articles"
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.get(username=self.kwargs["author"]).articles.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = getCategoryList()
        return context

class CategoryView(ListView):
    template_name = "article/index.html"
    paginate_by = 10
    context_object_name = "articles"

    def get_queryset(self):
        return Category.objects.get(title = self.kwargs["category"]).articleList.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = getCategoryList()
        return context

class SearchView(ListView):
    template_name = "article/index.html"
    paginate_by = 10
    context_object_name = "articles"
    def get_queryset(self):
        return Article.objects.filter(title__contains = self.request.GET["title"])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = getCategoryList()
        return context

class ArticleView(CreateView):
    template_name = "article/article.html"
    form_class = CommentForm
    success_url = "/"
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Article.objects.get(slug = self.kwargs["slug"]).comments.all()
        return context

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.author = self.request.user
        new_form.article = Article.objects.get(slug = self.kwargs["slug"])
        new_form.save()
        return super().form_valid(form)

class ProfileChange(UpdateView):
    template_name = "article/profile.html"
    form_class = UserProfileForm
    success_url = "/profile/"
    
    def form_valid(self, form):
        user_change = CustomUserChangeForm(self.request.POST, instance = self.request.user)
        if user_change.is_valid():
            user_change.save()
        messages.success(self.request, "Profiliniz Başarıyla Değiştirildi!")
        return super().form_valid(form)
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_change_form"] = CustomUserChangeForm(instance = self.request.user)
        return context

    def get_object(self):
        return UserProfile.objects.get(user = self.request.user)
