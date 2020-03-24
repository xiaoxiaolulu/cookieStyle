"""
DESCRIPTION：News Models 测试案例

    Covering the auxiliary function method:
         def __str__(self):
         def switch_like(self, user)
         def get_parent(self)
         def get_children(self)
         def reply_this(self, user, text)
         def likers_count(self)
         def get_likers(self)
         def replies_count(self)

:Created by Null.
"""
from test_plus import TestCase
from test.news.models import News


class NewsModelsTest(TestCase):

    def setUp(self):
        self.user1 = self.make_user(username='user01', password="123456")
        self.user2 = self.make_user(username='user02', password="123456")
        self.news1 = News.objects.create(user=self.user1, content="我是第一条")
        self.news2 = News.objects.create(user=self.user1, content="我是第二条")
        # reply True 是否为评论
        self.news3 = News.objects.create(user=self.user2, content="我是第一条的回复", reply=True, parent=self.news1)

    def test__str__(self):
        """
        __str__方法测试用例
        """
        self.assertEqual(self.news1.__str__(), "我是第一条")

    def test__switch_like(self):
        """
        点赞/取消测试用例
        """
        self.news1.switch_like(self.user2)
        # 点赞数测试
        assert self.news1.likers_count() == 1
        self.news1.switch_like(self.user1)
        assert self.news1.likers_count() == 2
        # user1/2 是否在点赞用户集合中
        assert self.user1 in self.news1.get_likers()
        assert self.user2 in self.news2.get_likers()
        # 取消点赞
        self.news1.switch_like(self.user1)
        assert self.user1 not in self.news1.get_likers()
        assert self.news1.likers_count() == 1

    def test_replay_this(self):
        """
        回复测试用例
        """
        initial_count = News.objects.count()
        self.news1.reply_this(self.user2, "第二次回复")
        assert News.objects.count() == initial_count + 1
        assert self.news1.replies_count() == 2
        assert self.news3 in self.news1.get_children()

