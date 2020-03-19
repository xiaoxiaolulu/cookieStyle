from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    nickname = models.CharField(null=True, blank=True, max_length=255, verbose_name='昵称')
    job_title = models.CharField(max_length=50, null=True, blank=True, verbose_name='职称')
    introduction = models.TextField(blank=True, null=True, verbose_name='简介')
    picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name='头像')
    address = models.CharField(max_length=50, null=True, blank=True, verbose_name='住址')
    birthday = models.DateField(verbose_name='生日', blank=True, null=True)
    personal_url = models.URLField(max_length=255, null=True, blank=True, verbose_name='个人链接')
    weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name='微博链接')
    zhihu = models.URLField(max_length=255, null=True, blank=True, verbose_name='知乎链接')
    github = models.URLField(max_length=255, null=True, blank=True, verbose_name='GitHub链接')
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name='LinkedIn链接')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def get_profile_name(self):
        if self.nickname:
            return self.nickname
        return self.username
