from django.conf import settings
from django.db import models

from .thread import Thread


class ThreadSubscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscribed_threads')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_subscribers')
