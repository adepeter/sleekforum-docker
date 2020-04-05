from django import forms

from flyapps.threads.models import Post


class BasePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class PostForm(BasePostForm):
    pass


class PostEditForm(BasePostForm):
    pass
