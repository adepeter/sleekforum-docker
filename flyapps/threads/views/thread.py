from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from ...categories.models import Category
from ..forms.post import PostForm
from ..forms.thread import ThreadCreationForm, ThreadEditForm
from ..forms.thread_share import ThreadShareForm
from ..models import Thread

TEMPLATE_URL = 'flyapps/threads/thread'


class ListThread(SingleObjectMixin, ListView):
    slug_url_kwarg = 'category_slug'
    template_name = f'{TEMPLATE_URL}/list_threads.html'
    context_object_name = 'threads'
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.threads.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        context['threads'] = self.object_list
        return context


class CreateThread(CreateView):
    model = Thread
    form_class = ThreadCreationForm
    template_name = f'{TEMPLATE_URL}/create_thread.html'

    def form_valid(self, form):
        form.instance.starter = self.request.user
        form.instance.category = self.category
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug__iexact=self.kwargs['category_slug'])
        return super().dispatch(request, *args, **kwargs)


class ReadThread(MultipleObjectMixin, CreateView):
    query_pk_and_slug = True
    form_class = PostForm
    paginate_by = 1
    template_name = f'{TEMPLATE_URL}/read_thread.html'
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        self.thread = self.get_object()
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        thread = super().get_object(
            Thread.objects.filter(category__slug__iexact=self.kwargs['category_slug'])
        )
        return thread

    def post(self, request, *args, **kwargs):
        self.thread = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return self.thread.posts.all()

    def get_context_data(self, **kwargs):
        context = super(ReadThread, self).get_context_data(**kwargs)
        context['thread'] = self.thread
        return context

    def form_valid(self, form):
        form.instance.thread = self.thread
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pass


class EditThread(UpdateView):
    model = Thread
    form_class = ThreadEditForm
    query_pk_and_slug = True
    template_name = f'{TEMPLATE_URL}/edit_thread.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])


class DeleteThread(DeleteView):
    model = Thread

    def get_success_url(self):
        kwargs = {
            'category': self.kwargs['category_slug']
        }
        return reverse('flyapps:threads:list_threads', kwargs=kwargs)


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
