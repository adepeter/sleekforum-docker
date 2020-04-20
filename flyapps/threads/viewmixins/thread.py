from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.core.exceptions import ImproperlyConfigured, FieldDoesNotExist
from django.views.generic.detail import SingleObjectMixin

from ...miscs.models.activity import Action
from ...miscs.viewmixins.activity import BaseActivityActionView

from ..models.thread import Thread


class SingleBooleanObjectMixin:
    """
    This mixin cannot be implemented on its own.
    Must be called with a view
    """
    boolean_field = ''

    def get_boolean_field(self):
        if not self.boolean_field:
            raise ImproperlyConfigured('You must set boolean_field attribute on this view')
        return self.validate_boolean_field(self.boolean_field)

    def validate_boolean_field(self, boolean_field):
        fields = [field.name for field in self.model._meta.get_fields()]
        if boolean_field not in fields:
            raise FieldDoesNotExist('%(field_name)s does not seem to be a valid field on the supplied %(model)s' % {
                'model': self.model._meta.model_name,
                'field_name': self.boolean_field})
        else:
            return boolean_field

    def get_boolean_value(self, obj=None):
        if obj is None:
            obj = self.get_object()
        boolean_field = self.get_boolean_field()
        boolean_value = getattr(obj, boolean_field)
        if not isinstance(boolean_value, bool):
            raise TypeError('The return boolean field isnt an bool')
        return boolean_value

    def toggle_boolean_and_save(self, obj, value=None, value_reverse=True):
        if value is None:
            value = self.get_boolean_value(obj)
        field = self.get_boolean_field()
        new_value = not value if value_reverse else value
        setattr(obj, field, new_value)
        obj.save()
        return obj


class ThreadSingleActionMiscView(SingleBooleanObjectMixin, SingleObjectMixin, View):
    redirect_to_threads = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.misc_action = self.toggle_boolean_and_save(self.object)
        return self.get_success_url()

    def get_success_url(self):
        if self.redirect_to_threads is None:
            raise ImproperlyConfigured(
                '\'redirect_to_threads\' class attr cannot be set to None. Attribute must be set to a boolean')
        else:
            if self.redirect_to_threads is True:
                return redirect(reverse('flyapps:threads:list_threads', args=[str(self.kwargs['category_slug'])]))
            return redirect(self.object.get_absolute_url())


class LikeDislikeThreadMixin(LoginRequiredMixin, BaseActivityActionView):
    model = Thread
    activity_model = Action
    activity_field_name = 'action_value'
    field_exclusion = True
    excluded_fields = [Action.UP_VOTE, Action.DOWN_VOTE, Action.FAVORITE]


class FavoriteThreadMixin(LikeDislikeThreadMixin):
    field_exclusion = False
    excluded_fields = []
