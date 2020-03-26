from django.urls import path
from test.quora import views


app_name = "quora"

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='all_questions'),
    path('correct_answered_questions', views.AnsweredQuestionListView.as_view(), name='correct_answered_questions'),
    path('uncorrect_answered_questions', views.UnAnsweredQuestionListView.as_view(), name='uncorrect_answered_questions'),
    path('ask_question/', views.QuestionCreateView.as_view(), name="ask_question"),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name="question_detail"),
    path('create_answer/<int:question_id>/', views.AnswerCreateView.as_view(), name="create_answer")
]
