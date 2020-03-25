from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from test.blogs.forms import ArticleForm
from test.blogs.models import Article, ArticleCategory
from test.utils.core import AuthorRequiredMixin


class ArticleListView(ListView):

    model = Article
    paginate_by = 5
    context_object_name = 'article_list'
    template_name = 'blogs/article_list.html'

    def get_queryset(self):
        return Article.objects.get_published()

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleListView, self).get_context_data(*args, **kwargs)
        context['articles_categories'] = ArticleCategory.objects.all()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):

    model = Article
    form_class = ArticleForm
    template_name = 'blogs/article_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView, self).form_valid(form)

    def get_success_url(self):
        # 闪现消息
        message = '您的文章已经创建成功！'
        messages.success(self.request, message)
        return reverse_lazy('blogs:list')


class DraftListView(ArticleListView):

    def get_queryset(self, **kwargs):
        return Article.objects.get_drafts()


class ArticleDetailView(DetailView):

    model = Article
    template_name = 'blogs/article_detail.html'
    context_object_name = 'article'


class ArticleUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):

    model = Article
    form_class = ArticleForm
    template_name = 'blogs/article_update_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleUpdateView, self).form_valid(form)

    def get_success_url(self):
        # 闪现消息
        message = '您的文章已经更新成功！'
        messages.success(self.request, message)
        return reverse_lazy('blogs:detail', kwargs={"slug": self.get_object().slug})
