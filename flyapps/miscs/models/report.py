from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ...rules.models import Rule
from ..behaviours.content_types import ContentTypeMixin


class Violation(ContentTypeMixin):
    rule = models.ForeignKey(
        Rule,
        verbose_name=_('violated rule'),
        on_delete=models.CASCADE,
        related_name='violations'
    )
    is_violated = models.BooleanField(_('accept violation'), default=False)
    reported_on = models.DateTimeField(verbose_name=_('reported on'), default=timezone.now)

    def is_violated(self):
        return self.is_violated