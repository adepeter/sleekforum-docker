from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView, UpdateView

from ..forms.thread_share import ThreadShareForm
from ..models import Thread

TEMPLATE_URL = 'flyapps/threads/thread'


class HideThread(UpdateView):
    model = Thread
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object.get_absolute_url())

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])

    def get_object(self):
        thread = super().get_object()
        thread.is_hidden = True
        thread.save()
        return thread


class LockThread(UpdateView):
    pass


class ReportThread(UpdateView):
    pass


class ShareThread(SingleObjectMixin, FormView):
    model = Thread
    form_class = ThreadShareForm
    template_name = f'{TEMPLATE_URL}/share_thread.html'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(category__slug__iexact=self.kwargs['category_slug'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

    def get_success_url(self):
        kwargs = {
            'category_slug': self.object.category.slug,
            'pk': self.object.id,
            'slug': self.object.slug
        }
        return reverse('flyapps:threads:read_thread', kwargs=kwargs)


class UnhideThread(UpdateView):
    pass


class UnlockThread(UpdateView):
    pass


def hide_thread(request, category_slug, pk, slug):
    thread = get_object_or_404(Thread, category__slug__iexact=category_slug, pk=pk, slug__iexact=slug)
    thread.is_hidden = True
    return redirect(thread.get_absolute_url())
