from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView
from test.quora.forms import QuestionForms
from test.quora.models import Question, Answer, Vote
from test.utils.core import ajax_required


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

    def get_queryset(self):
        return Question.objects.select_related('user').filter(pk=self.kwargs['pk'])


class AnswerCreateView(LoginRequiredMixin, CreateView):

    model = Answer
    fields = ['content', ]
    template_name = 'quora/answer_create_form.html'

    def get_context_data(self, **kwargs):
        context = super(AnswerCreateView, self).get_context_data()
        context['question'] = Question.objects.get(pk=self.kwargs['question_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super(AnswerCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "您的问题已经创建")
        return reverse_lazy('quora:question_detail', kwargs={"pk": self.kwargs['question_id']})


@login_required
@ajax_required
@require_http_methods(['POST'])
def question_vote(request):
    question_id = request.POST["questionId"]
    value = True if request.POST['value'] == 'U' else False
    question = Question.objects.get(pk=question_id)
    users = question.votes.values_list('user', flat=True)
    if request.user.pk in users and (question.votes.get(user=request.user).value == value):
        question.votes.get(user=request.user).delete()
    else:
        question.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes": question.total_votes()})


@login_required
@ajax_required
@require_http_methods(['POST'])
def answer_vote(request):
    answer_id = request.POST["answerId"]
    value = True if request.POST['value'] == 'U' else False
    answer = Answer.objects.get(pk=answer_id)
    users = answer.votes.values_list('user', flat=True)
    if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
        answer.votes.get(user=request.user).delete()
    else:
        answer.votes.update_or_create(user=request.user, defaults={"value": value})
    return JsonResponse({"votes": answer.total_votes()})


@login_required
@ajax_required
@require_http_methods(['POST'])
def accept_answer(request):

    answer_id = request.POST['answerId']
    answer = Answer.objects.get(pk=answer_id)
    if answer.question.user.username != request.user.username:
        raise PermissionDenied
    answer.accept_answer()
    return JsonResponse({"status": "true"})
