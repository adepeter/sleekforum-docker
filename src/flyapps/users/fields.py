from django import forms
from django.utils.translation import gettext_lazy as _


class SexRadioButtonField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = _('Select sex')
        self.choices = (
            ('m', _('Male')),
            ('f', _('Female')),
        )
        self.widget = forms.RadioSelect(choices=self.choices)
        self.error_message = _('You must select a sex')



class BirthdayDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        EMPTY_LABELS = [
            _('Year'),
            _('Month'),
            _('Day')
        ]
        YEARS = [x for x in range(1960, 2012)]
        super().__init__(*args, **kwargs)
        self.label = _('Birthday')
        self.required = True
        self.error_messages = {
            'required': _('You must select your birthday'),
        }
        self.widget = forms.SelectDateWidget(
            empty_label=EMPTY_LABELS,
            years=YEARS
        )
