from django.contrib import admin
from test.blogs.models import Article, ArticleCategory
from mdeditor.widgets import MDEditorWidget
from django.db import models


class ArticleCategoryAdmin(admin.ModelAdmin):

    list_display = ['catname', 'created_at', 'updated_at']


class ArticleAdmin(admin.ModelAdmin):

    # formfield_overrides = {
    #     models.TextField: {'widget':  MDEditorWidget}
    # }
    list_display = ['slug', 'title', 'user', 'category', 'status', 'created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
