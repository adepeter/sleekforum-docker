from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from ...miscs.models.activity import Action
from ...miscs.viewmixins.activity import BaseActivityActionView

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


class UpDownVotePostMixin(LoginRequiredMixin, BasePostMixin, BaseActivityActionView):
    activity_model = Action
    activity_field_name = 'action_value'
    field_exclusion = True
    excluded_fields = [Action.LIKE, Action.DISLIKE, Action.FAVORITE]