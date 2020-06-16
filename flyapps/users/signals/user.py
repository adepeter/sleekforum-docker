from django.contrib import messages
from django.contrib.auth import user_logged_out as base_user_logged_out
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


@receiver(base_user_logged_out)
def user_logged_out(sender, request, user, **kwargs):
    print(request, user)
    if user is not None:
        message = _('Dear %(user)s, you have been \
        successfully logged out') % {'user': user.get_display_name}
        messages.success(request, message)
