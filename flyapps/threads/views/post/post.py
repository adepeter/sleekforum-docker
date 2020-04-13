from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ...forms.post import PostEditForm, PostForm
from ...models.post import Post
from ...viewmixins.post import BasePostMixin

TEMPLATE_URL = 'flyapps/threads/post'


class EditPost(BasePostMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = f'{TEMPLATE_URL}/edit_post.html'


class DeletePost(DeleteView):
    model = Post


class ReplyPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = f'{TEMPLATE_URL}/reply_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent'] = self.get_object()
        return context

    def form_valid(self, form):
        parent_object = self.get_object()
        form.instance.thread = parent_object.thread
        form.instance.parent = parent_object
        form.instance.user = self.request.user
        return super().form_valid(form)
