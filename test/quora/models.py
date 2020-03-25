import uuid
from collections import Counter
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from taggit.managers import TaggableManager
from test.users.models import User


class Vote(models.Model):

    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE, verbose_name='用户')
    value = models.BooleanField(default=True, verbose_name='赞同或反对')
    content_type = models.ForeignKey(ContentType, related_name='votes_on', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    vote = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '投票'
        verbose_name_plural = verbose_name


class QuestionQuerySet(models.query.QuerySet):
    """自定义QuerySet，提高模型类的可用性"""

    def get_answered(self):
        """已有答案的问题"""
        return self.filter(has_correct=True)

    def get_unanswered(self):
        """未被的回答的问题"""
        return self.filter(has_correct=False)

    def get_counted_tags(self):
        """统计所有问题标签的数量(大于0的)"""
        tag_dict = {}
        for obj in self.all():
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


class Question(models.Model):

    STATUS = (("O", "Open"), ("C", "Close"), ("D", "Draft"))
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE, verbose_name='提问者')
    title = models.CharField(max_length=255, unique=True, verbose_name='问题标题')
    slug = models.SlugField(max_length=255, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(max_length=1, choices=STATUS, default='0', verbose_name='问题状态')
    content = models.TextField(verbose_name='问题内容')
    tags = TaggableManager(help_text='多个标签使用, (英文)隔开', verbose_name='标签')
    has_correct = models.BooleanField(default=False, verbose_name='是否有正确回答')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
    votes = GenericRelation(Vote, verbose_name='投票情况')

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at", "-created_at")

    def __str__(self):
        return self.title

    def get_all_answers(self):
        return Answer.objects.filter(question=self)

    def count_answers(self):
        return self.get_all_answers().count()

    def get_accepted_answer(self):
        return Answer.objects.filter(question=self, is_accepted=True)

    def get_upvoters(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        return [vote.user for vote in self.votes.filter(value=False)]

    def total_votes(self):
        # return len(self.get_upvoters()) - len(self.get_downvoters())
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]


class Answer(models.Model):

    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='问题')
    content = models.TextField(verbose_name='答案内容')
    is_accepted = models.BooleanField(default=False, verbose_name='是否被接受')
    votes = GenericRelation(Vote, verbose_name='投票情况')
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '答案'
        verbose_name_plural = verbose_name
        ordering = ("-updated_at", "-created_at")

    def __str__(self):
        return self.uuid_id.__str__()

    def get_upvoters(self):
        return [vote.user for vote in self.votes.filter(value=True)]

    def get_downvoters(self):
        return [vote.user for vote in self.votes.filter(value=False)]

    def total_votes(self):
        # return len(self.get_upvoters()) - len(self.get_downvoters())
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]
