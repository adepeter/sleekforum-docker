from django.db import models
from django.utils.translation import gettext_lazy as _

from ..behaviours.content_types import ContentTypeMixin
from ..managers.activity import ActivityManager


class Action(ContentTypeMixin):
    FAVORITE = 'FAV'
    LIKE = 'LIK'
    DISLIKE = 'DSL'
    UP_VOTE = 'UVT'
    DOWN_VOTE = 'DVT'

    ACTION_CHOICES = (
        (FAVORITE, _('Favorite')),
        (LIKE, _('Like')),
        (DISLIKE, _('Dislike')),
        (UP_VOTE, _('Up Vote')),
        (DOWN_VOTE, _('Down Vote')),
    )

    action_value = models.CharField(
        verbose_name=_('Action'),
        max_length=3,
        choices=ACTION_CHOICES
    )

    objects = ActivityManager()

    def __str__(self):
        return f'{self.user.username} just {self.get_action_value_display()}d {self.content_object}'

    class Meta:
        verbose_name_plural = _('Activities')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'action_value', 'content_type', 'object_id'],
                name='unique_user_activity'
            )
        ]