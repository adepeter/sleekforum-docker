from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Rule(models.Model):
    GLOBAL_RULE = 0
    FORUM_RULE = 1
    USER_RULE = 2

    RULE_CHOICES = (
        (GLOBAL_RULE, _('Global Rule')),
        (FORUM_RULE, _('Forum Rule')),
        (USER_RULE, _('User Rule')),
    )

    category = models.IntegerField(
        verbose_name=_('rule category'),
        choices=RULE_CHOICES,
        default=GLOBAL_RULE
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name='rules'
    )
    name = models.CharField(verbose_name=_('name'), max_length=255)
    description = models.TextField(verbose_name=_('description'))
    show = models.BooleanField(verbose_name=_('show rule'), default=True)

    def __str__(self):
        return f'{self.name} - {self.get_category_display()}'
