from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db import connection
from .models import Article,Category, UserProfile
from .forms import CommentForm, UserProfileForm, CustomUserChangeForm
from django.core import serializers
# Create your views here.
def getCategoryList():
    """
        Kategorileri Veritabanından Çeker.
    """
    categoryList = Category.objects.all()
    return categoryList

def paginate(request, lists, perPage):
    paginator = Paginator(lists, perPage)

    page = request.GET.get('page') or 1
    return paginator.get_page(page)

# /
def index(request):
    """
        İndex Sayfası
    """
    article_list = Article.objects.all()
    
    articles = paginate(request, article_list, 10)

    category_list = getCategoryList()
    return render(request, "article/index.html", {"articles":articles, "categories":category_list})

# /about
def about(request):
    """
        Hakkımda Sayfası

    """
    category_list = getCategoryList()
    return render(request, "article/about.html", {"categories":category_list})

# /article/<slug>
def getArticleBySlug(request, slug):
    article = Article.objects.get(slug = slug)
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.author = request.user
        comment.save()
        return JsonResponse({"data":"success"})

    category_list = getCategoryList()
    context = {
        'comment_form':comment_form,
        'article':article,
        'comments':article.comments.all(),
        'categories':category_list
    }

    return render(request, "article/article.html", context)

# /author/<authorName>
def getArticleByAuthor(request, author):
    author = User.objects.get(username = author)
    author_article_list = author.articles.all()
    category_list = getCategoryList()
    articles = paginate(request, author_article_list, 10)
    return render(request, "article/index.html", {"articles":articles, "categories":category_list})

# /category/<categoryName>
def getArticleByCategory(request, category):
    category = Category.objects.get(title = category)

    article_list = category.articleList.all()
    category_list = getCategoryList()

    articles = paginate(request, article_list, 10)
    
    return render(request, "article/index.html", {"articles":articles, "categories":category_list})

# /search/s
def searchArticleByTitle(request):
    title = request.GET["title"]
    article = Article.objects.filter(title__contains = title)
    category_list = getCategoryList()
    return render(request, "article/index.html", {"articles":article, "categories":category_list})

def changeProfileInformation(request):
    user = UserProfile.objects.get(user= request.user)
    
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST or None, request.FILES, instance=user )
        user_change_form  = CustomUserChangeForm(request.POST or None, instance = request.user)
        if user_profile_form.is_valid() and user_change_form.is_valid():
            user_profile_form.save()
            user_change_form.save()
            messages.success(request, "Profiliniz Başarıyla Güncellendi.")
            return redirect("/")
    else:
        user_profile_form = UserProfileForm(instance = user)
        user_change_form  = CustomUserChangeForm(instance  = request.user)
    return render(request, "article/profile.html", {"user_profile_form":user_profile_form, "user_change_form":user_change_form})
