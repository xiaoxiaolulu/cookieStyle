from django.contrib import admin
from test.quora.models import Vote, Question, Answer


class VoteAdmin(admin.ModelAdmin):

    list_display = ["uuid_id", "user", "value", "content_type", "object_id"]


class QuestionAdmin(admin.ModelAdmin):

    list_display = ["id", 'user', "title", "slug", "status", "tags", "has_correct"]


class AnswerAdmin(admin.ModelAdmin):

    list_display = ["uuid_id", "user", "question", "is_accepted"]


admin.site.register(Vote, VoteAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
