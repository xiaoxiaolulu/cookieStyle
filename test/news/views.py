from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DeleteView
from test.news.models import News
from test.utils.core import ajax_required, AuthorRequiredMixin


class NewsListView(LoginRequiredMixin, ListView):

    # model = News
    # queryset = News.objects.filter(reply=False).all()
    paginate_by = 10
    template_name = 'news/news_list.html'

    def get_queryset(self, **kwargs):
        return News.objects.filter(reply=False).all()


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_news(request):

    newsContent = request.POST['news_content'].strip()
    if newsContent:
        news = News.objects.create(user=request.user, content=newsContent)
        html = render_to_string('news/news_single.html', {'news': news, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不能为空")


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):

    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy("news:list")  # 在项目的URLConf未加载前使用


@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):

    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({"likes": news.likers_count()})
