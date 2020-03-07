from django.conf import settings
from django.db import models

from .thread import Thread


class ThreadView(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_views')
    viewed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thread_views')
    viewers = models.TextField()
    views = models.PositiveIntegerField(default=0)
