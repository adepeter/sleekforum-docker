from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
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


class InboxMessage(SingleObjectMixin, ListView):
    template_name = f'{TEMPLATE_URL}/new_inbox.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.user = get_user(self.request)
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(User, **{self.slug_field + str('__iexact'): self.user.slug})

    def get_queryset(self):
        return self.object.messages()


class StartMessage(CreateView):
    model = User
    form_class = MessageCreationForm
    template_name = f'{TEMPLATE_URL}/start_message.html'
    slug_url_kwarg = 'recipient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipient'] = self.get_object()
        if self.similar_starter():
            context['similar_starter'] = self.similar_starter()
            messages.info(self.request, _('Dear %s, you cannot send message to yourself') % self.request.user.username)
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


class ReplyMessage(MultipleObjectMixin, CreateView):
    model = Message
    form_class = MessageReplyForm
    template_name = f'{TEMPLATE_URL}/reply_message.html'
    query_pk_and_slug = True
    # slug_field =
    slug_url_kwarg = 'recipient'
