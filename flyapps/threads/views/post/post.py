from django.shortcuts import redirect
from django.views.generic.edit import UpdateView, DeleteView

from ...forms.post import PostEditForm
from ...models.post import Post

TEMPLATE_URL = 'flyapps/threads/post'


class EditPost(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = f'{TEMPLATE_URL}/edit_post.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__slug__iexact=self.kwargs['thread_slug'])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_hidden:
            return redirect(self.request.META.get('HTTP_REFERER'))
        return super().dispatch(request, *args, **kwargs)


class DeletePost(DeleteView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__slug__iexact=self.kwargs['thread_slug'])

    def get_success_url(self):
        pass
