from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ...managers.post import PostManager
from ...models.thread import Thread


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('post'),
        on_delete=models.SET_NULL,
        null=True
    )
    thread = models.ForeignKey(
        Thread,
        verbose_name=_('thread'),
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(verbose_name=_('Post content'))
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(verbose_name=_('likes'), default=0)
    dislikes = models.PositiveIntegerField(
        verbose_name=_('dislikes'),
        default=0
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        related_name='+',
        null=True,
        blank=True
    )

    objects = PostManager()

    def get_absolute_url(self):
        kwargs = {
            'category_slug': self.thread.category.slug,
            'slug': self.thread.slug,
            'pk': self.thread.id
        }
        return reverse(
            'flyapps:threads:read_thread',
            kwargs=kwargs
        ) + '?page=last'

    def get_edit_url(self):
        kwargs = {
            'thread_slug': self.thread.slug,
            'pk': self.id,
        }
        return reverse(
            'flyapps:threads:post:edit_post',
            kwargs=kwargs
        )

    def get_delete_url(self):
        kwargs = {
            'thread_slug': self.thread.slug,
            'pk': self.id,
        }
        return reverse(
            'flyapps:threads:post:delete_post',
            kwargs=kwargs
        )

    def get_reply_to_url(self):
        kwargs = {
            'thread_slug': self.thread.slug,
            'pk': self.id,
        }
        return reverse(
            'flyapps:threads:post:reply_post',
            kwargs=kwargs
        )

    def __str__(self):
        return f'{self.content[:10]} by {self.user.username} to {self.thread.title}'