from django.urls import path
from django.views.generic import TemplateView

from test.blogs import views


app_name = "blogs"
urlpatterns = [
    path("", views.ArticleListView.as_view(), name="list"),
    path("article_create/", views.ArticleCreateView.as_view(), name='create')
]
