from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class ThreadShareForm(forms.Form):
    recipient = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': _('Enter receiver e-mail address'),
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread')
        super().__init__(*args, **kwargs)
        self.fields['message'].initial = str(self.thread.content)

    def share_thread(self, **kwargs):
        cleaned_data = self.cleaned_data
        sender = 'noreply@mail.com'
        recipient = cleaned_data['recipient']
        subject = self.thread.title
        message = cleaned_data['message']
        return send_mail(subject, message, sender, [recipient])
