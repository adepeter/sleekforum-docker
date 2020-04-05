from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, FormView, UpdateView

from ....categories.models import Category
from ...forms.thread.thread_share import ThreadShareForm
from ...forms.thread.thread_search import ThreadSearchForm
from ...models.thread import Thread
from ...viewmixins.thread import ThreadSingleActionMiscView

TEMPLATE_URL = 'flyapps/threads/thread/thread_misc'


class LockUnlockThread(ThreadSingleActionMiscView):
    model = Thread
    boolean_field = 'is_locked'
    redirect_to_threads = False


class HideUnhideThread(ThreadSingleActionMiscView):
    model = Thread
    boolean_field = 'is_hidden'
    redirect_to_threads = False


class ReportThread(UpdateView):
    pass


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['thread'] = self.object
        return kwargs

    def get_queryset(self):
        return self.model.objects.filter(category__slug__iexact=self.kwargs['category_slug'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        if form.share_thread():
            messages.success(self.request, 'Post was shared successfully')
        return super().form_valid(form)

    def get_success_url(self):
        kwargs = {
            'category_slug': self.object.category.slug,
            'pk': self.object.id,
            'slug': self.object.slug
        }
        return reverse('flyapps:threads:read_thread', kwargs=kwargs)


class ListThreadParticipant(SingleObjectMixin, ListView):
    template_name = f'{TEMPLATE_URL}/list_thread_participant.html'
    query_pk_and_slug = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(Thread.objects.filter(category__slug__iexact=self.kwargs['category_slug']))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.participants.all()


class ThreadLikeUnlike:
    pass


@login_required
def like_unlike_thread(request, category_slug, pk, slug, **kwargs):
    from django.shortcuts import get_object_or_404
    from ...models.thread.thread_like_dislike import ThreadLikeDislike
    like_action = kwargs.get('likeunlike', None)
    base_value = ThreadLikeDislike.LIKE if like_action == 'like' else ThreadLikeDislike.DISLIKE
    thread = get_object_or_404(Thread, category__slug__iexact=category_slug, pk=pk, slug__iexact=slug)
    try:
        user_like = ThreadLikeDislike.objects.get(thread=thread, user=request.user)
        user_like_value = user_like.value
        if like_action == 'like':
            if user_like_value == base_value:
                user_like.delete()
            else:
                user_like.value = base_value
                user_like.save()
        else:
            if user_like_value == base_value:
                user_like.delete()
            else:
                user_like.value = base_value
                user_like.save()
    except ThreadLikeDislike.DoesNotExist:
        ThreadLikeDislike.objects.create(thread=thread, user=request.user, value=base_value)