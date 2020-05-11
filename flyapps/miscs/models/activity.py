from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..behaviours.content_types import ContentTypeMixin
from ..managers.activity import ActivityManager
from ..signals.activity import activity_updater


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

    def signal_emitter(self):
        """
        Custom signal for updating user actions
        Emits action_value and object type of instance been created/deleted
        """
        ct = ContentType.objects.get_for_model(self.content_object)
        obj = ct.get_object_for_this_type(id=self.object_id)
        activity_updater.send(
            sender=self.__class__,
            action_value=self.action_value,
            obj=obj
        )

    def delete(self):
        """ Signal is called again to know the object been deleted """
        self.signal_emitter()
        super().delete()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        """ Signal is called to know the object been created """
        self.signal_emitter()

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
