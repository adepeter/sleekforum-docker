from django import forms
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(forms.Form):
    error_messages = {
        'password_mismatch': _('Passwords do not match')
    }

    email = forms.EmailField(label=_('E-mail'))
    username = forms.CharField(label=_('Username'))
    password_1 = forms.CharField(label=_('Password'), strip=False)
    password_2 = forms.CharField(label=_('Repeat password'), strip=False)

    def __init__(self, *args, **kwargs):
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

    def clean_password_2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')
        if password_1 and password_2 and (password_1 != password_2):
            raise forms.ValidationError(self.error_messages['password_mismatch'], code='password_mismatch')