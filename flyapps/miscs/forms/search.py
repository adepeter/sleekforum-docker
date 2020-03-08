from django import forms
from django.utils.translation import gettext_lazy as _


class BaseSearchForm(forms.Form):
    text = forms.CharField(label=_('text'))

class CategorySearchForm(BaseSearchForm):
    pass

class ThreadSearchForm(BaseSearchForm):
    pass

class UserSearchForm(BaseSearchForm):
    pass