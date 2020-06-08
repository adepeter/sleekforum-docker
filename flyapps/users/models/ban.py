from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Ban(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='+'
    )
    banned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_superuser': True},
        on_delete=models.DO_NOTHING,
        related_name='banned_users'
    )
    sections = models.ManyToManyField(
        'categories.Category',
        related_name='bans'
    )
    message = models.TextField(verbose_name=_('Ban message'))
    expiry = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} has been banned'
