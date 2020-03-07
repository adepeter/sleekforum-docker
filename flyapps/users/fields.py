from django import forms

class SexRadioButtonField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        super(SexRadioButtonField, self).__init__(*args, ** kwargs)
        self.error_message = 'You must select a sex'
        self.choices = (
            ('male', 'Male'),
            ('female', 'Female'),
        )
        self.label = 'Select sex'
        self.widget = forms.RadioSelect(choices=self.choices)