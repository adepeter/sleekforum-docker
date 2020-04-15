from ....miscs.forms import BaseViolationForm
from ....rules.models import Rule


class ThreadViolationForm(BaseViolationForm):
    allowed_categories = [Rule.FORUM_RULE, 2, 0]
    """
    Just for fun. Parent class is at module root
    """

    def repeat_reported_rules(self):
        return self.unique_rules_queryset
