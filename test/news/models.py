import uuid
from django.db import models
from django.conf import settings


class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='publishes', verbose_name='用户')
    content = models.TextField(verbose_name='新闻内容')
    likers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='liked_news',
                                    verbose_name='点赞用户')
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name='children',
                               verbose_name='父级自关联')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return self.content
