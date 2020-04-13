from django.shortcuts import redirect

from ..models.post import Post


class BasePostMixin:
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(thread__slug__iexact=self.kwargs['thread_slug'])

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_hidden:
            return redirect(self.request.META.get('HTTP_REFERER'))
        return super().dispatch(request, *args, **kwargs)
