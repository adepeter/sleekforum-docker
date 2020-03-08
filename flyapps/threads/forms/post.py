from django import forms
from ..models import Post


class BasePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class PostForm(BasePostForm):
    pass