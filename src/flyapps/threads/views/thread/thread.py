import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from ....categories.models import Category

from ...forms.post import PostForm
from ...forms.thread import ThreadCreationForm, ThreadEditForm

from ...models.thread import Thread, ThreadView

from ...signals import thread_views_creator_and_updater

TEMPLATE_URL = 'flyapps/threads/thread'

User = get_user_model()


class ListThread(SingleObjectMixin, ListView):
    slug_url_kwarg = 'category_slug'
    template_name = f'{TEMPLATE_URL}/list_threads.html'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.threads.unhidden_threads()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context


class CreateThread(CreateView):
    model = Category
    slug_url_kwarg = 'category_slug'
    form_class = ThreadCreationForm
    template_name = f'{TEMPLATE_URL}/create_thread.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.starter = self.request.user
        form.instance.category = self.get_object()
        form.instance.views += 1
        ThreadView.objects.create(
            thread=form.save(),
            user=self.request.user
        )
        return super().form_valid(form)


class ReadThread(MultipleObjectMixin, CreateView):
    query_pk_and_slug = True
    form_class = PostForm
    paginate_by = 5
    template_name = f'{TEMPLATE_URL}/read_thread.html'
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        self.thread = self.get_object()
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        thread = super().get_object(
            Thread.objects.filter(
                category__slug__iexact=self.kwargs['category_slug']
            )
        )
        if self.request.user.is_authenticated:
            viewers = thread.thread_views.filter(user=self.request.user)
            if not viewers.exists():
                ThreadView.objects.create(thread=thread, user=self.request.user)
                thread.views += 1
                thread.save()
        return thread

    def post(self, request, *args, **kwargs):
        self.thread = self.get_object()
        self.object_list = self.get_queryset()
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return self.thread.posts.all()

    def get_context_data(self, **kwargs):
        context = super(ReadThread, self).get_context_data(**kwargs)
        context['thread'] = self.thread
        context['liked_by'] = [liked_by.user for liked_by in self.thread.actions.filter_action_by('LIK')]
        context['disliked_by'] = [disliked_by.user for disliked_by in self.thread.actions.filter_action_by('DSL')]
        context['frequent_posters'] = User.objects.filter(
            post__in=self.object_list,
            post__is_hidden=False
        ).annotate(num_of_posts=Count('post')).order_by('-num_of_posts')
        return context

    def form_valid(self, form):
        form.instance.thread = self.thread
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        page_kwargs = self.request.GET.get(self.page_kwarg)
        if page_kwargs or self.get_paginate_by(self.object_list):
            kwargs = {
                'category_slug': self.kwargs['category_slug'],
                'pk': self.thread.id,
                'slug': self.thread.slug,
            }
            context = self.get_context_data()
            paginator = context['paginator']
            num_pages = paginator.num_pages
            return reverse('flyapps:threads:read_thread', kwargs=kwargs) + '?%(page_kwargs)s=%(last_page)d' % {
                'page_kwargs': self.page_kwarg,
                'last_page': num_pages
            }
        return super().get_success_url()


class EditThread(UpdateView):
    model = Thread
    form_class = ThreadEditForm
    query_pk_and_slug = True
    template_name = f'{TEMPLATE_URL}/edit_thread.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(category__slug__iexact=self.kwargs['category_slug'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['thread'] = self.object
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        thread = self.get_object()
        if thread.starter != self.request.user:
            return render(request, 'flyapps/threads/auth/unauthorised_edit.html')
        return super().dispatch(request, *args, **kwargs)


class DeleteThread(DeleteView):
    model = Thread

    def get_success_url(self):
        kwargs = {
            'category': self.kwargs['category_slug']
        }
        return reverse('flyapps:threads:list_threads', kwargs=kwargs)


class ListNewestThread(ListView):
    model = Thread
    template_name = f'{TEMPLATE_URL}/newest_threads.html'
    paginate_by = 10
    context_object_name = 'threads'

    def get(self, request, *args, **kwargs):
        messages.info(
            self.request,
            _('Dear %(login)s, you are viewing newest threads that were created 7days ago') % {
                'login': self.request.user.username if self.request.user.is_authenticated else 'guest'
            }
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model._meta.default_manager.unhidden_threads(
            created__gte=timezone.now() - datetime.timedelta(days=7)
        )


class ListTrendingThread(ListView):
    model = Thread
    template_name = f'{TEMPLATE_URL}/trending_threads.html'
    paginate_by = 10
    context_object_name = 'threads'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            num_of_hidden_posts=Count('posts__is_hidden')
        ).exclude(
            num_of_hidden_posts__gte=10
        ).order_by('-pin', '-num_of_hidden_posts')[:100]