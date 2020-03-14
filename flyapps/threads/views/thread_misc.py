from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View, ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, FormView, UpdateView

from ..forms.thread_share import ThreadShareForm
from ..forms.thread_search import ThreadSearchForm
from ..models import Thread
from ...categories.models import Category

TEMPLATE_URL = 'flyapps/threads/thread/thread_misc'


class HideThread(SingleObjectMixin, View):
    model = Thread
    redirect_to_threads = False
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_hidden = True
        self.object.save()
        return self.get_success_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])

    def get_success_url(self):
        if self.redirect_to_threads:
            return redirect(reverse('flyapps:threads:list_threads', args=[str(self.kwargs['category_slug'])]))
        return redirect(self.object.get_absolute_url())


class LockThread(SingleObjectMixin, View):
    http_method_names = ['get']
    model = Thread
    redirect_to_threads = True
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_locked = True
        self.object.save()
        return self.get_success_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])

    def get_success_url(self):
        if self.redirect_to_threads:
            return redirect(reverse('flyapps:threads:list_threads', args=[str(self.kwargs['category_slug'])]))
        return redirect(self.object.get_absolute_url())


class ReportThread(UpdateView):
    pass  # pip install --upgrade asgiref bokeh click pyaml pygments setuptools virtualenv wrapt


class SearchThread(SingleObjectMixin, FormMixin, ListView):
    model = Thread
    template_name = f'{TEMPLATE_URL}/search_thread.html'
    form_class = ThreadSearchForm
    paginate_by = 2
    slug_url_kwarg = 'category_slug'
    ordering = 'created'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Category.objects.all())
        self.search_query = self.request.GET.get('keyword')
        self.check_content = self.request.GET.get('check_content')
        self.object_list = None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset().filter(category__slug__iexact=self.kwargs['category_slug'])
        if self.search_query:
            if self.check_content:
                return qs.filter(Q(title__icontains=self.search_query) | Q(content__icontains=self.search_query))
            return qs.filter(title__icontains=self.search_query)
        return qs.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        context['search_query'] = self.search_query
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['category'] = self.object
        return kwargs


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
    model = Thread
    redirect_to_threads = False
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_hidden = False
        self.object.save()
        return self.get_success_url()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])

    def get_success_url(self):
        if self.redirect_to_threads:
            return redirect(reverse('flyapps:threads:list_threads', args=[str(self.kwargs['category_slug'])]))
        return redirect(self.object.get_absolute_url())


class UnlockThread(UpdateView):
    http_method_names = ['get']
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


class ListThreadParticipant(SingleObjectMixin, ListView):
    template_name = f'{TEMPLATE_URL}/list_thread_participant.html'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Thread.objects.filter(category__slug__iexact=self.kwargs['category_slug']))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.participants.all()
