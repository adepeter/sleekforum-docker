from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...miscs.utils.text import generate_random_string

from ..validators import validate_unique_user, validate_username_chars

User = get_user_model()


class BaseUserAdminForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'),
        max_length=255,
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Please enter your password'),
        }),
        help_text=_('If not supplied, 20 random characters are randomly for you')
    )

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'is_staff',
            'is_superuser',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)


class UserAdminCreationForm(BaseUserAdminForm):

    def clean_username(self):
        cleaned_username = self.cleaned_data['username']
        validate_unique_user('This username must be unique', username=cleaned_username)
        return cleaned_username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].validators.append(validate_username_chars)

    def clean_password(self):
        cleaned_password = self.cleaned_data['password']
        if not cleaned_password:
            cleaned_password = self.make_random_password()
        return cleaned_password

    def make_random_password(self, length=20):
        return generate_random_string(length, allow_special_chars=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = user.set_password(self.cleaned_data['password'])
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user


class UserAdminChangeForm(BaseUserAdminForm):
    password = ReadOnlyPasswordHashField()

    class Meta(BaseUserAdminForm.Meta):
        fields = BaseUserAdminForm.Meta.fields + [
            'password'
        ]

    def clean_password(self):
        return self.initial['password']