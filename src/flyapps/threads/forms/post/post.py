from django import forms
from django.utils.translation import gettext_lazy as _

from flyapps.threads.models import Post


class BasePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': '5',
            'placeholder': _('Let\'s get started')
        })


class PostForm(BasePostForm):
    pass


class PostEditForm(BasePostForm):
    pass
