from django.contrib import admin
from test.blogs.models import Article, ArticleCategory


class ArticleCategoryAdmin(admin.ModelAdmin):

    list_display = ['catname', 'created_at', 'updated_at']


class ArticleAdmin(admin.ModelAdmin):

    list_display = ['slug', 'title', 'user', 'category', 'status', 'created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
