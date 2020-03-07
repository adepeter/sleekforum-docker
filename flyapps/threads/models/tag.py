from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _

class ThreadTag(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=100, unique=True)
    slug = models.SlugField(verbose_name=_('slug'), editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']