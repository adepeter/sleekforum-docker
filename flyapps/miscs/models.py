from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Activity(models.Model):
    FAVORITE = 'F'
    LIKE = 'L'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'

    ACTIVITY_CHOICES = (
        (FAVORITE, _('Favorite')),
        (LIKE, _('Like')),
        (UP_VOTE, _('Up Vote')),
        (DOWN_VOTE, _('Down Vote')),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activities = models.CharField(verbose_name=_('Actions'), max_length=1, choices=ACTIVITY_CHOICES)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        verbose_name_plural = _('Activities')
        constraints = [
            models.UniqueConstraint(fields=['user', 'activities'], name='unique_activity')
        ]
