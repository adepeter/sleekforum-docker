from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Ban(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL
    )
    banned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_superuser': True}
    )
    sections = models.ManyToManyField(
        ContentType,
        related_name='bans'
    )
    message = models.TextField(verbose_name=_('Ban message'))
    until = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} has been banned'
