from ....miscs.forms import BaseViolationForm
from ....rules.models import Rule


class ThreadViolationForm(BaseViolationForm):

    allowed_categories = [Rule.FORUM_RULE]

    """
    Just for fun. Parent class is at module root
    """
