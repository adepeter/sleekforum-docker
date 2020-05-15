from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .exceptions import DuplicateDataEntryError


class Message(models.Model):
    starter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='messages_started')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='messages_received')
    text = models.TextField(verbose_name=_('text'), unique_for_date='created')
    is_replied = models.BooleanField(verbose_name=_('is replied?'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.starter == self.recipient:
            raise DuplicateDataEntryError('You cannot send a message to yourself')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.starter.username} just started' \
               f' a correspondence with {self.recipient.username}'


class Reply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='replies')
    text = models.TextField(verbose_name=_('text'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.sender.username} just replied to {self.message}'

    class Meta:
        verbose_name = _('Reply')
        verbose_name_plural = _('Replies')
