from django import forms
from django.utils.translation import gettext_lazy as _


class ThreadSearchForm(forms.Form):
    keyword = forms.CharField(label=_('Keywords'))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(self, *args, **kwargs)
