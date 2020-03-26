from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from test.quora.forms import QuestionForms
from test.quora.models import Question


class QuestionListView(ListView):

    model = Question
    paginate_by = 20
    context_object_name = 'question_list'
    template_name = 'quora/question_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context['popular_tags'] = Question.objects.get_counted_tags()
        context['active'] = 'all'
        return context


class AnsweredQuestionListView(QuestionListView):

    def get_queryset(self):
        return Question.objects.get_answered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context['active'] = 'correct_answered'
        return context


class UnAnsweredQuestionListView(QuestionListView):

    def get_queryset(self):
        return Question.objects.get_unanswered()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuestionListView, self).get_context_data()
        context['active'] = 'uncorrect_answered'
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):

    model = Question
    form_class = QuestionForms
    template_name = 'quora/question_create_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "问题已提交")
        return reverse_lazy('quora:all_questions')


class QuestionDetailView(DetailView):

    model = Question
    context_object_name = 'question'
    template_name = 'quora/question_detail.html'
    query_pk_and_slug = True
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
