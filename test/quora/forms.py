from django import forms
from markdownx.fields import MarkdownxFormField
from test.quora.models import Question


class QuestionForms(forms.ModelForm):

    content = MarkdownxFormField()

    class Meta:

        model = Question
        fields = ["title", "content", "tags", "status"]
