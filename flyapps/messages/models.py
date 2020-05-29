from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..miscs.shortcuts import is_similar_objects as is_same_recipient

from .exceptions import DuplicateDataEntryError


class Message(models.Model):
    FLAG_NEW = 0
    FLAG_ACTIVE = 1
    FLAG_ACTIVE_AND_NEW = 2

    FLAG_CHOICES = [
        (FLAG_NEW, _('New')),
        (FLAG_ACTIVE, _('Active')),
        (FLAG_ACTIVE_AND_NEW, _('Active and New')),
    ]

    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Sender'),
        on_delete=models.DO_NOTHING,
        related_name='messages_started'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Receiver'),
        on_delete=models.DO_NOTHING,
        related_name='messages_received'
    )
    text = models.TextField(
        verbose_name=_('text'),
        unique_for_date='created'
    )
    flag = models.PositiveSmallIntegerField(
        verbose_name=_('flag'),
        choices=FLAG_CHOICES,
        default=FLAG_ACTIVE_AND_NEW
    )
    is_replied = models.BooleanField(
        verbose_name=_('is replied?'),
        default=False
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'starter': self.starter.slug,
        }
        return reverse('flyapps:messages:read_reply_message', kwargs=kwargs)

    def save(self, *args, **kwargs):
        if is_same_recipient(self.starter, self.recipient) is True:
            raise DuplicateDataEntryError('You cannot send a message to yourself')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.starter.username} just started' \
               f' a correspondence with {self.recipient.username}'


class Reply(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='replies'
    )
    text = models.TextField(verbose_name=_('text'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        kwargs = {'pk': self.message.id}
        if self.message.recipient == self.sender:
            kwargs.update({'starter': self.sender.slug})
        return reverse('flyapps:messages:read_reply_message', kwargs=kwargs)

    def __str__(self):
        return f'{self.sender.username} just replied to {self.message}'

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')


class MessageView(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='message_views'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_views'
    )
    created = models.DateTimeField(auto_now_add=True)
