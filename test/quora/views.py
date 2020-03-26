from django.shortcuts import render
from django.views.generic import ListView
from test.quora.models import Question


class QuestionListView(ListView):

    model = Question
    paginate_by = 20
    context_object_name = 'question_list'
    template_name = 'quora/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context['popular_tags'] = Question.objects.get_counted_tags()
        return context


class AnsweredQuestionListView(QuestionListView):

    def get_queryset(self):
        return Question.objects.get_answered()


class UnAnsweredQuestionListView(QuestionListView):

    def get_queryset(self):
        return Question.objects.get_unanswered()
