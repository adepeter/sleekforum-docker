from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...rules.models import Rule
from ..behaviours.content_types import ContentTypeMixin


class Violation(ContentTypeMixin):
    PENDING = 0
    ACCEPT = 1
    REJECT = 2

    PENALTY_NOTHING = 0
    PENALTY_HIDE = 1
    PENALTY_BAN = 2
    PENALTY_BAN_AND_DELETE = 3

    VIOLATION_CHOICES = (
        (PENDING, _('Awaiting actions')),
        (ACCEPT, _('Accepted violation')),
        (REJECT, _('Rejected violation')),
    )

    PENALTY_CHOICES = (
        (PENALTY_NOTHING, _('No action')),
        (PENALTY_HIDE, _('Hide object')),
        (PENALTY_BAN, _('Ban user')),
        (PENALTY_BAN_AND_DELETE, _('Delete object and Ban User')),
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
    penalty = models.IntegerField(
        verbose_name=_('penalty'),
        default=PENALTY_NOTHING,
        choices=PENALTY_CHOICES,
        help_text=_('Proper measure to be taken against violation'),
    )

    def __str__(self):
        return f'{self.user.username} just reported {self.content_object} for violating {self.rules}'
