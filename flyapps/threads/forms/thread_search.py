from django import forms
from django.utils.translation import gettext_lazy as _


class ThreadSearchForm(forms.Form):
    keyword = forms.CharField(label=_('Keywords'), max_length=50)
    check_content = forms.BooleanField(required=False, help_text=_('Search keyword in thread content too'))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.category = kwargs.pop('category')
        super().__init__(*args, **kwargs)
        self.fields['keyword'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'size': 10,
            'placeholder': _('Search in %(category)s' % {'category': self.category.slug})
        })

        if self.request.GET:
            self.fields['keyword'].initial = self.request.GET.get('keyword')
            self.fields['check_content'].initial = self.request.GET.get('check_content')
