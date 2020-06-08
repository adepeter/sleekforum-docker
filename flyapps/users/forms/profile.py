from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from ..fields import BirthdayDateField, SexRadioButtonField

User = get_user_model()


class UserSearchForm(forms.Form):
    keyword = forms.CharField(
        label=_('E-mail or username'),
        help_text=_('Kindly enter \
        the e-mail, username or profile display name of user')
    )


class UserProfileEditForm(forms.ModelForm):
    sex = SexRadioButtonField()
    dob = BirthdayDateField()

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'dob',
            'sex',
            'location',
            'signature',
            'facebook',
            'twitter',
            'github',
            'website',
            'about'
        ]

class UserPasswordChangeForm(forms.ModelForm):
    pass