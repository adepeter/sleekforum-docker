from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Message, Reply


class BaseMessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.similar_starter = kwargs.pop('similar_starter', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = None
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('Enter your message here')
            })
        }


class MessageCreationForm(BaseMessageForm):
    class Meta(BaseMessageForm.Meta):
        model = Message

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.similar_starter is True:
            del self.fields['status']
            self.fields['text'].widget.attrs.update({'disabled': True})


class MessageReplyForm(BaseMessageForm):
    class Meta(BaseMessageForm.Meta):
        model = Reply

    def __init__(self, *args, **kwargs):
        if kwargs.get('similar_starter'):
            del kwargs['similar_starter']
        super().__init__(*args, **kwargs)
