from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ....categories.models import Category
from ....miscs.models import Action, Violation
from ...managers.thread import ThreadManager


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
    pin = models.IntegerField(verbose_name=_('pin thread'), choices=PIN_CHOICES, default=PIN_DEFAULT)
    prefix = models.IntegerField(verbose_name=_('prefix'), choices=PREFIX_CHOICES, default=PREFIX_DEFAULT)
    slug = models.SlugField(verbose_name=_('slug'), blank=True, editable=False, db_index=True)
    content = models.TextField(verbose_name=_('content'), unique_for_date='created')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(verbose_name=_('lock thread'), default=False)
    is_hidden = models.BooleanField(verbose_name=_('hide thread'), default=False)
    is_editable = models.BooleanField(verbose_name=_('allow edit'), default=True)

    shares = models.PositiveIntegerField(verbose_name=_('total shares'), default=0)
    views = models.PositiveIntegerField(default=0)

    actions = GenericRelation(Action, related_query_name='threads')
    violations = GenericRelation(Violation, related_query_name='violations')

    objects = ThreadManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_likes_count(self):
        return self.actions.filter_action_by('LIK').count()

    def get_dislikes_count(self):
        return self.actions.filter_action_by('DSL').count()

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['id', 'slug'])
        ]
        ordering = ['-modified']

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

    def get_dislike_url(self):
        return reverse('flyapps:threads:dislike_thread', kwargs=self.get_kwargs())

    def get_like_url(self):
        return reverse('flyapps:threads:like_thread', kwargs=self.get_kwargs())

    def get_report_url(self):
        return reverse('flyapps:threads:report_thread', kwargs=self.get_kwargs())

    def get_share_url(self):
        return reverse('flyapps:threads:share_thread', kwargs=self.get_kwargs())

    def toggle_hide(self):
        return reverse('flyapps:threads:toggle_hide_thread', kwargs=self.get_kwargs())

    def toggle_lock(self):
        return reverse('flyapps:threads:toggle_lock_thread', kwargs=self.get_kwargs())
