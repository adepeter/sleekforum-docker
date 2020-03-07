from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail


class ThreadShareForm(forms.Form):
    receiver = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': _('Enter receiver e-mail address'),
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_email(self):
        send_mail(
            'Shared successfully',
            'This is a shared post',
            'adepeter26@gmail.com',
            ['adeboy@gmail.com'],
            fail_silently=False
        )