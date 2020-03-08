from django import forms
from django.utils.translation import gettext_lazy as _
from ..models import Thread


class BaseThreadForm(forms.ModelForm):
    error_messages = {
        'title': {
            'unique': _('This title already exist'),
            'required': _('This field cannot be left empty')
        },

    }

    class Meta:
        model = Thread
        fields = ['title', 'prefix', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'aria-describedby': 'titleHelp',
                'placeholder': _('Enter thread title')
            }),
            'content': forms.Textarea(attrs={
                'rows': 15,
                'class': 'form-control',
                'placeholder': _('Let\'s get started'),
            })
        }


class ThreadCreationForm(BaseThreadForm):

    class Meta(BaseThreadForm.Meta):
        help_texts = {
            'title': _('Describe your topic well, while keeping the subject as short as possible.'),
        }


class ThreadEditForm(BaseThreadForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.thread = kwargs.pop('thread')
        super().__init__(*args, **kwargs)
        if self.request.user != self.thread.starter or not self.request.user.is_staff:
            fields = ['title', 'content', 'prefix', 'tags']
            for f in fields:
                self.fields[f].widget.attrs.update({'disabled': True})

    def save(self, commit=True):
        new_thread = super().save(commit=False)
        if commit:
            new_thread.save()
        return new_thread