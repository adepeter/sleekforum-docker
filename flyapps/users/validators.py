from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def validate_uniqueness(username):
    user_exist = User.objects.get_by_username_or_email(username)
    if user_exist:
        raise ValidationError(_('%(name)s is already taken' % {'name': username, }))


def validate_unique_user(error_message, **criteria):
    existent_user = User.objects.filter(**criteria)
    if existent_user:
        raise ValidationError(error_message)