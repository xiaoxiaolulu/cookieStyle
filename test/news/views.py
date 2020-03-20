from django.shortcuts import render
from django.views.generic import ListView
from test.news.models import News


class NewsListView(ListView):

    # model = News
    # queryset = News.objects.filter(reply=False).all()
    paginate_by = 10
    template_name = 'news/news_list.html'

    def get_queryset(self, **kwargs):
        return News.objects.filter(reply=False).all()
