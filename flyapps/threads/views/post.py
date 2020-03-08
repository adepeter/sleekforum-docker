from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, DeleteView
from ..forms.post import PostForm
from ..models import Post

TEMPLATE_URL = 'flyapps/threads/post'


class EditPost(UpdateView):
    model = Post
    form_class = PostForm
    template_name = f'{TEMPLATE_URL}/edit_post.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__slug__iexact=self.kwargs['thread_slug'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['post'] = self.object
        return kwargs


class DeletePost(DeleteView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__slug__iexact=self.kwargs['thread_slug'])

    def get_success_url(self):
        pass
