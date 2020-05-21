from django import template
from django.db.models import Q
from django.template.defaultfilters import stringfilter
from django.utils.translation import gettext_lazy as _

from ...miscs.utils.text import truncator as truncate_message

from ..models import Message
from ..shortcuts import get_last_reply_for_message

register = template.Library()

TEMPLATE_URL = 'flyapps/messages/_partials'


@register.simple_tag
def get_latest_reply_or_message(message):
    """ Returns latest message or reply for a correspondence """
    return get_last_reply_for_message(message)


@register.simple_tag
def is_instance_of_message(instance):
    """Check if the instance parameter is a message object"""
    return isinstance(instance, Message)


@register.inclusion_tag(f'{TEMPLATE_URL}/active_correspondence.html')
def active_messages_with_inclusion_tag(user, title='Active mailbag'):
    """
    This template tag uses django templatetag inclusion principle
    The template tag receives a user object for the messages it wants show.
    And returns queryset (ie Message queryset) for active chats.
    And writes it to the context

    In summary, it returns all current conversation (Started/replied/non-replied)
    for the supplied user
    """
    messages = Message.objects.filter(
        Q(starter=user) |
        Q(recipient=user, flag__in=[Message.FLAG_NEW, Message.FLAG_ACTIVE])
    )
    context = {
        'title': _(title),
        'messages': messages,
        'user': user
    }
    return context


@register.inclusion_tag(f'{TEMPLATE_URL}/newest_correspondence.html')
def newest_messages_with_inclusion_tag(user, title='Inbox'):
    """
    This template tag uses django templatetag inclusion principle
    The template tag receives a user object for the messages it wants show.
    And returns queryset (ie Message queryset) for newly created messages or new reply
    And writes it to the context

    In summary, it returns new inbox for the supplied user
    """
    messages = Message.objects.filter(
        Q(recipient=user, flag=Message.FLAG_ACTIVE_AND_NEW) |
        Q(flag=Message.FLAG_ACTIVE)
    ).exclude(replies__sender=user)
    context = {
        'title': _(title),
        'messages': messages,
        'user': user
    }
    return context


@register.simple_tag
def newest_message(user):
    """
    This return a new_inbox queryset.
    Serves similar function as newest_messages_with_inclusion_tag()
    """
    return user.messages_received.exclude(flag=Message.FLAG_ACTIVE)


@register.filter(name='truncate_message')
@stringfilter
def truncate_text(message_text, word_count=20):
    """This template tag does the following function
    1. Receives a message obj from the template.
    2. And return the latest reply on that message object.
    3. If the message has no reply / replies, it returns the original message content.
    4. Above all, it truncates the message for readabilty.
    """
    return truncate_message(message_text, word_count)


@register.simple_tag(name='recipient_switcher')
def active_message_transposer(message, current_user):
    """
    function:
    If current user is message recipient, it switches the recipient to starter
    This is a typical feature that is found in chat start page.
    template tag must for use for active_message manipulation
    """
    starter = message.starter
    recipient = message.recipient
    if current_user == recipient:
        recipient = starter
    return recipient
