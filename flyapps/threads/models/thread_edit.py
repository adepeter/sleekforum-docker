from django.conf import settings
from django.db import models

from .thread import Thread


class ThreadEdit(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_edits')
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='thread_edits'
    )
    editor_name = models.CharField(max_length=255)
    editor_slug = models.SlugField()
    edits = models.PositiveSmallIntegerField(default=0)
    last_edit_on = models.DateTimeField(auto_now_add=True)
