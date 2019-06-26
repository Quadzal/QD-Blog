from django.contrib import admin
from .models import Article, Category, UserProfile

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "created_date", "author"]
    list_filter  = ["title", "created_date"]

admin.site.index_title = "ES Blog - Yönetici Paneli"
admin.site.site_title  = " "
admin.site.site_header = "ES Blog"

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)
