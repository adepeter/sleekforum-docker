from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView
from django.views.generic.list import MultipleObjectMixin
from django.utils.translation import gettext_lazy as _

from ..miscs.shortcuts import is_similar_objects as compare_users

from .forms import MessageCreationForm, MessageReplyForm
from .models import Message, Reply

TEMPLATE_URL = 'flyapps/messages'

User = get_user_model()


class InboxMessage(LoginRequiredMixin, SingleObjectMixin, ListView):
    template_name = f'{TEMPLATE_URL}/index.html'
    paginate_by = 10
    ordering = ['-modified']

    def get(self, request, *args, **kwargs):
        self.user = get_user(self.request)
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_slug_field(self):
        return super().slug_field + str('__iexact')

    def get_object(self):
        slug_field = self.get_slug_field()
        return get_object_or_404(User, **{slug_field: self.user.slug})

    def get_queryset(self):
        return self.object.messages_started.all()


class StartMessage(LoginRequiredMixin, CreateView):
    model = User
    form_class = MessageCreationForm
    template_name = f'{TEMPLATE_URL}/start_message.html'
    slug_url_kwarg = 'recipient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipient'] = self.get_object()
        if self.similar_starter():
            context['similar_starter'] = self.similar_starter()
            messages.info(
                self.request,
                _('Dear %s, you cannot send message to yourself') %\
                self.request.user.username
            )
        return context

    def similar_starter(self):
        "Check if message starter is message recipient"
        starter = self.request.user
        recipient = self.get_object()
        return compare_users(starter, recipient)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['similar_starter'] = self.similar_starter()
        return kwargs

    def form_valid(self, form):
        form.instance.starter = self.request.user
        form.instance.recipient = self.get_object()
        return super().form_valid(form)

    def get_success_url(self):
        pass


class ReadReplyMessage(MultipleObjectMixin, CreateView):
    model = Message
    form_class = MessageReplyForm
    template_name = f'{TEMPLATE_URL}/read_reply_message.html'
    paginate_by = 1
    query_pk_and_slug = True
    slug_url_kwarg = 'starter'

    def get(self, request, *args, **kwargs):
        self.message = self.get_object(Message.objects.all())
        if self.request.user != self.message.starter and \
                self.request.user != self.message.recipient:
            raise PermissionDenied
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.message.replies.all()

    def get_slug_field(self):
        return 'starter__slug__iexact'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        return context

    def form_valid(self, form):
        form.instance.message = self.message
        form.instance.sender = self.request.user
        return super().form_valid(form)
