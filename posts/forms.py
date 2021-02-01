from django import forms
from . import models
from users import models as user_models
from .models import Post
from django_summernote.widgets import SummernoteWidget


class SearchForm(forms.Form):
    title = forms.CharField(initial="", required=False)
    user = forms.ModelChoiceField(
        required=False, empty_label="Anyone", queryset=user_models.User.objects.all()
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
