from django import forms


class CommaSeparatedField(forms.Field):
    pass

class SwitchField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = forms.RadioSelect(attrs={'class': 'form-control'})
