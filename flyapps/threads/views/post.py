from django.views.generic.edit import CreateView
from ..forms.post import PostForm
from ..models import Post


class EditPost(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_comment'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__slug__iexact=self.kwargs['thread_slug'])
