import math
from datetime import datetime

from django import template
from django.utils.translation import ngettext, gettext_lazy as _
from ..models import ThreadView

register = template.Library()


@register.filter
def fetch_view_count(thread):
    try:
        thread_view = ThreadView.objects.filter(thread=thread)
        return thread_view.get().views
    except ThreadView.DoesNotExist:
        return 0


@register.filter
def time_ago(param):
    if isinstance(param, object):
        def timesince(self):
            now = datetime.now()
            diff = now - param
            if diff.day == 0 and diff.seconds > 0 and diff.seconds < 60:
                seconds = diff.seconds
                result = ngettext(_('(seconds)%d second ago'), _('(seconds)%d seconds ago') % {'seconds': seconds})
            elif diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes = math.floor(diff.seconds / 60)
                result = ngettext(_('(minutes)%d minute ago'), _('(minutes)%d minutes ago') % {'minutes': minutes})
            elif diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours = math.floor(diff.seconds / 3600)
                result = ngettext(_('(minutes)%d hour ago'), _('(minutes)%d hours ago') % {'hours': hours})
            elif diff.days >= 30 and (diff.days <= 365 or diff.days <= 366):
                months = math.floor(diff.days / 30)
                result = ngettext(_('(months)%d month ago'), _('(months)%d months ago') % {'months': months})
            else:
                years = math.floor(diff.days / 365)
                result = ngettext(_('(years)%d year ago'), _('(years)%d years ago') % {'years': years})
            return result
