from django.urls import path
from test.news import views


app_name = "news"
urlpatterns = [
    path("", views.NewsListView.as_view(), name='list'),
    path("post-news/", views.post_news, name='post_news'),
    path("delete/<str:pk>/", views.NewsDeleteView.as_view(), name='delete_news')
]
