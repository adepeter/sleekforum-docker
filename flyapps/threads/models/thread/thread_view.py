from django.conf import settings
from django.db import models
from django.utils import timezone

from .thread import Thread


class ThreadView(models.Model):
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name='thread_views'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='thread_views'
    )
    viewed_on = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['thread', 'user'],
                name='unique_thread_user_on_threadview'
            )
        ]
