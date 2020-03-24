from django.db import models
from django.db.models import Count
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager
from test.users.models import User


class ArticleCategory(models.Model):

    catname = models.CharField(max_length=50, verbose_name='类别名称')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return self.catname

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name


class ArticleQuerySet(models.query.QuerySet):

    """自定义查询集"""
    def get_published(self):
        return self.filter(status='P').order_by('-created_at')

    def get_drafts(self):
        return self.filter(status='D').order_by('-updated_at')

    def get_counted_tags(self):
        tag_dict = {}
        query = self.filter(status='P').annotate(tagged=Count('tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1
                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Article(models.Model):

    STATUS = (("D", "Draft"), ("P", "Published"))

    status = models.CharField(max_length=1, choices=STATUS, default='D', verbose_name='文章状态')
    category = models.ForeignKey(ArticleCategory, verbose_name='文章类别', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, related_name='author', on_delete=models.SET_NULL, verbose_name='作者')
    title = models.CharField(max_length=255, blank=False, null=False, unique=True, verbose_name='文章标题')
    cover = models.ImageField(upload_to='blogs/covers/%Y/%m/%d/', verbose_name='文章封面')
    abstract = models.TextField(null=True, blank=True, verbose_name='文章摘要', default='此文章没有摘要')
    content = MDTextField(default="", verbose_name='文章内容')
    slug = models.SlugField(max_length=255, null=True, verbose_name='(URL)别名', blank=True)
    tags = TaggableManager(help_text='多个标签使用英文逗号(,)隔开', verbose_name='文章标签')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
