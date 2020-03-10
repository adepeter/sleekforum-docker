import math

from django import template
from django.utils import timezone
from django.utils.translation import ngettext, gettext_lazy as _

register = template.Library()


@register.filter
def time_ago(param):
    if isinstance(param, object):
        now = timezone.now()
        diff = now - param
        if diff.days == 0 and diff.seconds > 0 and diff.seconds < 60:
            seconds = diff.seconds
            result = ngettext(_('%(seconds)d second ago'), _('%(seconds)d seconds ago'), seconds) % {
                'seconds': seconds
            }
        elif diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            result = ngettext(_('%(minutes)d minute ago'), _('%(minutes)d minutes ago'), minutes) % {
                'minutes': minutes
            }
        elif diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            result = ngettext(_('%(hours)d hour ago'), _('%(hours)d hours ago'), hours) % {
                'hours': hours
            }
        elif 30 <= diff.days <= 365 or diff:
            months = math.floor(diff.days / 30)
            result = ngettext(_('%(months)d month ago'), _('%(months)d months ago'), months) % {
                'months': months
            }
        else:
            years = math.floor(diff.days / 365)
            result = ngettext(_('%(years)d year ago'), _('%(years)d years ago'), years) % {
                'years': years
            }
        return result
