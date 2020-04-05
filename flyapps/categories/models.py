from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(verbose_name=_('name'), max_length=25)
    slug = models.SlugField(verbose_name=_('slug'), blank=True, db_index=True)
    description = models.TextField(verbose_name=_('description'), blank=True)
    is_lock = models.BooleanField(verbose_name=_('lock category'), default=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def get_description(self):
        if not self.description:
            return _('No description yet')
        return self.description

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'parent'], name='unique_name_parent'),
        ]
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    class MPTTMeta:
        order_insertion_by = ['name']
