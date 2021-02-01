from django import forms
from . import models
from users import models as user_models


class SearchForm(forms.Form):
    title = forms.CharField(initial="", required=False)
    user = forms.ModelChoiceField(
        required=False, empty_label="Anyone", queryset=user_models.User.objects.all()
    )
