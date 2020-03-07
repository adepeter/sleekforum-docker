from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import gettext_lazy as _


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.CharField(label=_('E-mail or username'),
                               widget=forms.TextInput(attrs={'placeholder': _('E-mail or username')}))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'placeholder': _('Password')}),
                               strip=False)

    def __init__(self, *args, request=None, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.request = request
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

    def confirm_login_allowed(self, user):
        pass
