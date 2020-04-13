import math

from django import template
from django.utils import timezone
from django.utils.translation import ngettext, gettext_lazy as _

register = template.Library()


@register.filter(expects_localtime=True)
def time_ago(param):
    if isinstance(param, object):
        now = timezone.now()
        diff = now - param
        if diff.days == 0 and 0 < diff.seconds < 60:
            seconds = diff.seconds
            result = ngettext(_('%(seconds)d second ago'),
                              _('%(seconds)d seconds ago'), seconds) % {
                         'seconds': seconds
                     }
        elif diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            result = ngettext(_('%(minutes)d minute ago'),
                              _('%(minutes)d minutes ago'), minutes) % {
                         'minutes': minutes
                     }
        elif diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            result = ngettext(_('%(hours)d hour ago'),
                              _('%(hours)d hours ago'), hours) % {
                         'hours': hours
                     }
        elif 1 <= diff.days <= 7:
            days = diff.days
            result = ngettext(_('%(days)d day ago'),
                              _('%(days)d days ago'), days) % {
                         'days': days
                     }
        elif 7 <= diff.days <= 30:
            weeks = math.floor(diff.days / 7)
            result = ngettext(_('%(weeks)d week ago'),
                              _('%(weeks)d weeks ago'), weeks) % {
                         'weeks': weeks
                     }
        elif 30 <= diff.days <= 365:
            months = math.floor(diff.days / 30)
            result = ngettext(_('%(months)d month ago'),
                              _('%(months)d months ago'), months) % {
                         'months': months
                     }
        else:
            years = math.floor(diff.days / 365)
            result = ngettext(_('%(years)d year ago'),
                              _('%(years)d years ago'), years) % {
                         'years': years
                     }
        return result


@register.filter
def pretty_count(value, decimal_place=1):
    try:
        if isinstance(value, int):
            views = str(value)
            if 3 <= len(views) <= 6:
                views = round(int(views) / 1000, decimal_place)
                result = '%(views)sk' % {'views': views}
            elif 6 <= len(views) <= 9:
                views = round(int(views) / 1000000, decimal_place)
                result = '%(views)sM' % {'views': views}
            else:
                result = views
            return result
    except TypeError:
        return f"You can't attach '{value}' to {pretty_count.__name__} because it is not instance of an int"