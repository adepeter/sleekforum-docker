from django.contrib import messages
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
        qs = super().get_queryset().filter(
            category__slug__iexact=self.kwargs['category_slug']
        )
        if self.search_query:
            if self.check_content:
                return qs.filter(
                    Q(title__icontains=self.search_query) |
                    Q(content__icontains=self.search_query)
                )
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
        return self.model.objects.filter(
            category__slug__iexact=self.kwargs['category_slug']
        )

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
        self.object = self.get_object(Thread.objects.filter(
            category__slug__iexact=self.kwargs['category_slug']
        ))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.participants.all()


def like_thread(request, category_slug, pk, slug):
    from django.shortcuts import get_object_or_404
    from django.contrib.contenttypes.models import ContentType
    from ....miscs.models import Action
    thread_obj = get_object_or_404(
        Thread,
        category__slug__iexact=category_slug,
        pk=pk, slug__iexact=slug
    )
    try:
        fetch_existing_thread_actions = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(thread_obj),
            object_id=thread_obj.id,
        ).exclude(action_value=Action.FAVORITE)
        fetch_existing_user_actions = fetch_existing_thread_actions.get(user=request.user)
        if fetch_existing_user_actions.action_value == 'D':
            fetch_existing_user_actions.action_value = 'L'
            fetch_existing_user_actions.save()
        else:
            fetch_existing_user_actions.delete()
    except Action.DoesNotExist:
        Action.objects.create(
            content_object=thread_obj,
            action_value='L',
            user=request.user
        )


def dislike_thread(request, category_slug, pk, slug):
    from django.shortcuts import get_object_or_404
    from django.contrib.contenttypes.models import ContentType
    from ....miscs.models import Action
    thread_obj = get_object_or_404(
        Thread,
        category__slug__iexact=category_slug,
        pk=pk,
        slug__iexact=slug
    )
    try:
        fetch_existing_thread_actions = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(thread_obj),
            object_id=thread_obj.id,
        )
        fetch_existing_user_actions = fetch_existing_thread_actions.get(user=request.user)
        if fetch_existing_user_actions.action_value_value == 'L':
            fetch_existing_user_actions.action_value = 'D'
            fetch_existing_user_actions.save()
        else:
            fetch_existing_user_actions.delete()
    except Action.DoesNotExist:
        Action.objects.create(
            content_object=thread_obj,
            action_value='D',
            user=request.user
        )


def favorite_thread(request, category_slug, pk, slug):
    from django.shortcuts import get_object_or_404
    from django.contrib.contenttypes.models import ContentType
    from ....miscs.models import Action
    thread_obj = get_object_or_404(
        Thread,
        category__slug__iexact=category_slug,
        pk=pk,
        slug__iexact=slug
    )
    try:
        fetch_thread_favorite_action = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(thread_obj),
            object_id=thread_obj.id,
            action_value='F',
            user=request.user
        )
        if fetch_thread_favorite_action:
            fetch_thread_favorite_action.delete()
    except Action.DoesNotExist:
        Action.objects.create(
            content_object=thread_obj,
            user=request.user,
            action_value=Action.FAVORITE
        )
