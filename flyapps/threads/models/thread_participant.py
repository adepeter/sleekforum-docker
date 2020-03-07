from django.conf import settings
from django.db import models

from .thread import Thread
from ..managers.thread import ThreadParticipantManager

class ThreadParticipant(models.Model):
    is_owner = models.BooleanField(default=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participants')

    objects = ThreadParticipantManager()