from django import forms
from django.utils.translation import gettext_lazy as _


class ThreadSearchForm(forms.Form):
    keyword = forms.CharField(label=_('Keywords'))
    check_content = forms.BooleanField(required=False, help_text=_('Search keyword in thread content too'))
    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        if self.request.GET:
            self.fields['keyword'].initial = self.request.GET.get('keyword')
            self.fields['check_content'].initial = self.request.GET.get('check_content')