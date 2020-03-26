from django.urls import path
from test.quora import views


app_name = "quora"

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='all_questions'),
    path('correct_answered_questions', views.AnsweredQuestionListView.as_view(), name='correct_answered_questions'),
    path('uncorrect_answered_questions', views.UnAnsweredQuestionListView.as_view(), name='uncorrect_answered_questions'),
    path('ask_question/', views.QuestionCreateView.as_view(), name="ask_question"),
    path('<int:pk>/<str:slug>/', views.QuestionDetailView.as_view(), name="question_detail")
]
