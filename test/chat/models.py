import uuid
from django.db import models
from test.users.models import User


class MessageQuerySet(models.query.QuerySet):

    def get_conversation(self, sender, reciever):
        qs_a2b = self.filter(sender=sender, reciever=reciever)
        qs_b2a = self.filter(sender=reciever, reciever=sender)
        return qs_a2b.union(qs_b2a).order_by('created_at')

    def get_most_recent_conversation_user(self, reciever):
        qs_sent = self.filter(sender=reciever)
        qs_received = self.filter(reciever=reciever)
        qs = qs_sent.union(qs_received).latest()
        if qs.sender == reciever:
            return qs.reciever
        return qs.sender


class Message(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    sender = models.ForeignKey(User, related_name='sent_messages', blank=True, null=True, on_delete=models.SET_NULL,
                               verbose_name='发送者')
    reverse = models.ForeignKey(User, related_name='recieved_messages', blank=True, null=True,
                                on_delete=models.SET_NULL, verbose_name='接受者')
    message = models.TextField(blank=True, null=True, verbose_name='私信内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    objects = MessageQuerySet.as_manager()

    class Meta:

        verbose_name = '私信'
        verbose_name_plural = verbose_name
        ordering = ('-created_at', )

    def __str__(self):
        return self.message

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()
