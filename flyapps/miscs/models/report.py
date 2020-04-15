from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...rules.models import Rule
from ..behaviours.content_types import ContentTypeMixin


class Violation(ContentTypeMixin):
    PENDING = 0
    ACCEPT = 1
    REJECT = 2

    VIOLATION_CHOICES = (
        (PENDING, _('Awaiting actions')),
        (ACCEPT, _('Accepted violation')),
        (REJECT, _('Rejected violation')),
    )
    rules = models.ManyToManyField(
        Rule,
        verbose_name=_('rules violated'),
        related_name='violations',
        related_query_name='violations'
    )
    is_violated = models.IntegerField(
        verbose_name=_('accept violation'),
        choices=VIOLATION_CHOICES,
        default=PENDING
    )
    reported_on = models.DateTimeField(
        verbose_name=_('reported on'),
        default=timezone.now
    )

    def __str__(self):
        return f'{self.user.username} just reported {self.content_object} for violating {self.rules}'
