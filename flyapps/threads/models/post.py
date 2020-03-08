from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..managers.post import PostManager
from .thread import Thread

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(verbose_name=_('Post content'))
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='+', null=True, blank=True)

    objects = PostManager()

    def get_absolute_url(self):
        kwargs = {
            'category_slug': self.thread.category.slug,
            'slug': self.thread.slug,
            'pk': self.thread.id
        }
        return reverse('flyapps:threads:read_thread', kwargs=kwargs)

    def get_edit_url(self):
        kwargs = {
            'thread_slug': self.thread.slug,
            'pk': self.id,
        }
        return reverse('flyapps:threads:post:edit_post', kwargs=kwargs)


    def get_delete_url(self):
        kwargs = {
            'thread_slug': self.thread.slug,
            'pk': self.id,
        }
        return reverse('flyapps:threads:post:delete_post', kwargs=kwargs)