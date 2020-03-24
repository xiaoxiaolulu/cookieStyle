from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from test.news.models import News


class NewsViewsTest(TestCase):

    def setUp(self):
        self.user = self.make_user("user01")
        self.other_user = self.make_user("user02")
        self.client = Client()
        self.other_client = Client()
        self.client.login(username='user01', password='password')
        self.other_client.login(username='user02', password='password')
        self.first_news = News.objects.create(
            user=self.user,
            content="第一条动态")
        self.second_news = News.objects.create(
            user=self.user,
            content="第二条动态"
        )
        self.third_news = News.objects.create(
            user=self.other_user,
            content="评论第一条动态",
            reply=True,
            parent=self.first_news
        )

    def test_news_list(self):
        response = self.client.get(reverse("news:list"))
        assert response.status_code == 200
        assert self.first_news in response.context['news_list']
        assert self.second_news in response.context['news_list']
        assert self.third_news not in response.context['news_list']

    def test_delete_news(self):
        initial_count = News.objects.count()
        response = self.client.post(reverse("news:delete_news", kwargs={"pk": self.second_news.pk}))
        assert response.status_code == 302
        assert News.objects.count() == initial_count - 1

    def test_post_news(self):
        initial_count = News.objects.count()
        response = self.client.post(reverse("news:post_news"), {'news_content': "hello"},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")  # 表示发送Ajax Request请求
        assert response.status_code == 302
        assert News.objects.count() == initial_count - 1

    def test_like_news(self):
        response = self.client.post(reverse("news:post_like"), {'newsId': self.first_news.pk},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")  # 表示发送Ajax Request请求
        assert response.status_code == 200
        assert self.first_news.likers_count() == 1
        assert self.user in self.first_news.get_likers()
        assert response.json()['likes']

    def test_get_children(self):
        response = self.client.get(reverse('news:get_replies'), {'newsId': self.first_news.pk},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")  # 表示发送Ajax R)
        assert response.status_code == 200
        assert response.json()['newsid'] == str(self.first_news.pk)
        assert self.first_news.content in response.json()['replies']
        assert '第一条动态' in response.json()['replies']

    def test_post_reply(self):
        response = self.client.get(reverse('news:post_like'),
                                   {'newsId': self.second_news.pk, 'replyContent': "回复第二条新闻"},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")  # 表示发送Ajax R)
        assert response.status_code == 200
        assert response.json()['newsid'] == str(self.second_news.pk)
        assert response.json()['replies_count'] == 1
