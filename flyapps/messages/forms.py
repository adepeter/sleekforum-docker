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
    STATE_ACTIVE = 'A'
    STATE_NEW = 'N'
    STATE_ACTIVE_NEW = 'AN'

    STATUS_CHOICES = (
        (STATE_NEW, _('New')),
        (STATE_ACTIVE, _('Active')),
        (STATE_ACTIVE_NEW, _('Active and New')),
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        initial=STATE_ACTIVE_NEW,
        widget=forms.HiddenInput
    )

    class Meta(BaseMessageForm.Meta):
        model = Message

    def __init__(self, *args, **kwargs):
        similar_starter = kwargs.pop('similar_starter')
        super().__init__(*args, **kwargs)
        if similar_starter is True:
            self.fields['text'].disabled = True
            self.fields['status'].disabled = True



class MessageReplyForm(BaseMessageForm):
    class Meta(BaseMessageForm.Meta):
        model = Reply
