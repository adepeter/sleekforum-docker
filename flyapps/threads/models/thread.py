import math
from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _, ngettext

from taggit.managers import TaggableManager

from ...categories.models import Category


class Thread(models.Model):
    PIN_DEFAULT = 0
    PIN_LOCALLY = 1
    PIN_GLOBALLY = 2

    PREFIX_DEFAULT = 0
    PREFIX_HELP = 1
    PREFIX_DISCUSSION = 2
    PREFIX_INFO = 3

    PREFIX_CHOICES = (
        (PREFIX_DEFAULT, _('Default')),
        (PREFIX_HELP, _('Help')),
        (PREFIX_DISCUSSION, _('Discussion')),
        (PREFIX_INFO, _('Info')),
    )

    PIN_CHOICES = (
        (PIN_DEFAULT, _('Do not pin thread')),
        (PIN_LOCALLY, _('Pin thread within category')),
        (PIN_GLOBALLY, _('Pin thread globally')),
    )

    starter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(verbose_name=_('title'), max_length=150, unique=True)
    prefix = models.IntegerField(verbose_name=_('prefix'), choices=PREFIX_CHOICES, default=PREFIX_DEFAULT)
    slug = models.SlugField(verbose_name=_('slug'), blank=True, editable=False, db_index=True)
    content = models.TextField(verbose_name=_('content'), unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(verbose_name=_('lock thread'), default=False)
    is_hidden = models.BooleanField(verbose_name=_('hide thread'), default=False)
    edits = models.PositiveSmallIntegerField(default=0)
    viewer = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+')
    tags = TaggableManager(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['id', 'slug'])
        ]
        ordering = ['title', 'modified']

    def get_create_url(self):
        return reverse('flyapps:threads:create_thread', args=(str(self.category.slug)))

    def get_kwargs(self):
        kwargs = {
            'category_slug': self.category.slug,
            'pk': self.id,
            'slug': self.slug,
        }
        return kwargs

    def get_absolute_url(self):
        return reverse('flyapps:threads:read_thread', kwargs=self.get_kwargs())

    def get_edit_url(self):
        return reverse('flyapps:threads:edit_thread', kwargs=self.get_kwargs())

    def get_delete_url(self):
        return reverse('flyapps:threads:delete_thread', kwargs=self.get_kwargs())

    def timesince(self):
        now = datetime.now()
        diff = now - self.created
        if diff.day == 0 and diff.seconds > 0 and diff.seconds < 60:
            seconds = diff.seconds
            result = ngettext(_('(seconds)%d second ago'), _('(seconds)%d seconds ago') % {'seconds': seconds})
        elif diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            result = ngettext(_('(minutes)%d minute ago'), _('(minutes)%d minutes ago') % {'minutes': minutes})
        elif diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            result = ngettext(_('(minutes)%d hour ago'), _('(minutes)%d hours ago') % {'hours': hours})
        elif diff.days >= 30 and (diff.days <= 365 or diff.days <= 366):
            months = math.floor(diff.days / 30)
            result = ngettext(_('(months)%d month ago'), _('(months)%d months ago') % {'months': months})
        else:
            years = math.floor(diff.days / 365)
            result = ngettext(_('(years)%d year ago'), _('(years)%d years ago') % {'years': years})
        return result
