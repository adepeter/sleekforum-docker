from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..validators import validate_unique_user, validate_username_chars

User = get_user_model()


class UserRegistrationForm(forms.Form):
    error_messages = {
        'password_mismatch': _('Passwords do not match')
    }

    email = forms.EmailField(label=_('E-mail'))
    username = forms.CharField(
        label=_('Username'),
        validators=[validate_username_chars]
    )
    password_1 = forms.CharField(label=_('Password'), strip=False)
    password_2 = forms.CharField(label=_('Repeat password'), strip=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'aria-describedby': 'basic-addon1',
            'placeholder': _('E-mail')
        })
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'aria-describedby': 'basic-addon1',
            'placeholder': _('Username')
        })
        self.fields['password_1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'aria-describedby': 'basic-addon1',
            'placeholder': _('Password')
        })
        self.fields['password_2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'aria-describedby': 'basic-addon1',
            'placeholder': _('Repeat password')
        })

    def clean_username(self):
        cleaned_username = self.cleaned_data['username']
        validate_unique_user(
            'The username "%(username)s" have already been taken' % \
            {'username': cleaned_username},
            username=cleaned_username
        )
        return cleaned_username

    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        validate_unique_user(
            'This email has already been taken',
            email=cleaned_email
        )
        return cleaned_email

    def clean_password_2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if password_1 and password_2 and (password_1 != password_2):
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )
        return password_2

    def save(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        password = self.cleaned_data['password_2']
        extra_fields = {
            'ip_address': self.request.META.get('REMOTE_ADDR'),

        }
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        return user
