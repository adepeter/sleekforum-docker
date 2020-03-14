from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.core.exceptions import ImproperlyConfigured, FieldDoesNotExist
from django.views.generic.detail import SingleObjectMixin

from ..models import Thread


class ThreadMiscActionMixin:
    redirect_to_threads = True
    boolean_field = ''

    def get_boolean_field(self):
        if not self.boolean_field:
            raise ImproperlyConfigured('You must set boolean_field attribute on this view')
        else:
            fields = [f.name for f in self.model._meta.fields]
            if self.boolean_field not in fields:
                raise FieldDoesNotExist('%(field_name) does not seem to be a valid field on the supplied model' % {
                    'field_name': self.boolean_field})
            else:
                return self.boolean_field

    def toggle_boolean(self, boolean_field):
        pass


class ThreadMiscActionView(SingleObjectMixin, View):
    model = Thread
    redirect_to_threads = False
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_locked = False
        self.object.save()
        return self.get_success_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])

    def get_success_url(self):
        if self.redirect_to_threads:
            return redirect(reverse('flyapps:threads:list_threads', args=[str(self.kwargs['category_slug'])]))
        return redirect(self.object.get_absolute_url())
