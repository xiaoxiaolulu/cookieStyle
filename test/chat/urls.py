from django.urls import path
from django.views.generic import TemplateView
from test.chat import views


app_name = "chat"

urlpatterns = [
    path('', TemplateView.as_view(template_name='pages/chat.html'), name='index')
]
