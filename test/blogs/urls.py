from django.urls import path
from django.views.generic import TemplateView

from test.blogs import views


app_name = "blogs"
urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/blogs.html"), name="list"),
]
