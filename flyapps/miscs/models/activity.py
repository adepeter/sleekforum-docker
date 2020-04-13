from django.db import models
from django.utils.translation import gettext_lazy as _

from ..behaviours.content_types import ContentTypeMixin


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

    action_value = models.CharField(verbose_name=_('Action'), max_length=3, choices=ACTION_CHOICES)

    class Meta:
        verbose_name_plural = _('Activities')