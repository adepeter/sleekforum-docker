from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm as BaseSetPasswordForm
)
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('E-mail or username')
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('E-mail or username'),
            'autocomplete': 'off'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Password'),
        })


class PasswordResetForm(BasePasswordResetForm):
    template_url = 'flyapps/users/auth/password'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = _('Ensure you enter the a valid \
        email address associated with the account as a mail \
        will be sent there')
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter email address'),
        })

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        get_by_email = User.objects.filter(email=cleaned_email)
        if not get_by_email.exists():
            raise forms.ValidationError(_('%s doesnt exist in our database') % cleaned_email)
        return cleaned_email

    def save(self, **kwargs):
        new_reset = super().save(**kwargs)
        subject_template_name = '%s/password_reset_subject.txt' % self.template_url
        email_template_name = '%s/password_reset_email.html' % self.template_url
        kwargs.update({
            'subject_template_name': subject_template_name,
            'email_template_name': email_template_name
        })
        return new_reset


class SetPasswordForm(BaseSetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        for field in self.fields:
            password_placeholder = _('Enter new password') if field == 'new_password1' \
                else _('Repeat new password')
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': password_placeholder
            })