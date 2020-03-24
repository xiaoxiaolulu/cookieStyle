from django import forms
from test.blogs.models import Article


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['category', 'title', 'abstract', 'content', 'cover', 'tags', 'status']
