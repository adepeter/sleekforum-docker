from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Message, Reply


class BaseMessageForm(forms.ModelForm):
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
        similar_starter = kwargs.pop('similar_starter')
        super().__init__(*args, **kwargs)
        if similar_starter is True:
            self.fields['text'].disabled = True


class MessageReplyForm(BaseMessageForm):
    class Meta(BaseMessageForm.Meta):
        model = Reply
