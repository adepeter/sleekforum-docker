from django.conf import settings
from django.db import models
from django.contrib.auth.models import Permission
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ..managers.role import RoleManager


class Role(models.Model):
    name = models.CharField(_('name'), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('users'),
        through='Roleship',
        related_name='roles',
        blank=True
    )
    slug = models.SlugField(verbose_name=_('slug'), blank=True, db_index=True)

    objects = RoleManager()

    def natural_key(self):
        return (self.name,)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('roles')
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_name_on_role'
            ),
        ]
        indexes = [
            models.Index(
                fields=['slug'],
                name='index_slug_on_role'
            )
        ]
        ordering = ['name']


class Roleship(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='roleships'
    )
    role = models.ForeignKey(
        Role,
        verbose_name=_('role'),
        on_delete=models.CASCADE,
        related_name='roleships'
    )
    created = models.DateField(auto_now_add=True)
    reason = models.TextField(
        verbose_name=_('Reason for role'),
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                name='unique_user_role_on_roleship'
            )
        ]
