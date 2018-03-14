from django import forms
from .models import MyEntry


class BlogForm(forms.ModelForm):
    class Meta:
        model = MyEntry
        fields = ["header", "body", "tags"]
