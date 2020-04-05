from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import gettext_lazy as _


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
