from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .thread import Thread


class ThreadLikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    LIKE_DISLIKE_CHOICES = (
        (LIKE, _('Like')),
        (DISLIKE, _('Dislike')),
    )

    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='likes_dislikes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes_dislikes')
    value = models.SmallIntegerField(choices=LIKE_DISLIKE_CHOICES)

    def __str__(self):
        option_value = 'liked' if ThreadLikeDislike.LIKE is self.value else 'disliked'
        return f'{self.user.username} {option_value} {self.thread.title}'

    class Meta:
        verbose_name = _('Thread like and dislike')
        verbose_name_plural = _('Thread likes and dislikes')
        constraints = [
            models.UniqueConstraint(fields=['thread', 'user'], name='unique_thread_user'),
            models.UniqueConstraint(fields=['thread', 'user', 'value'], name='unique_thread_user_value')
        ]
