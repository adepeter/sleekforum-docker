from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


def validate_unique_user(error_message, **criteria):
    existent_user = User.objects.filter(**criteria).exists()
    if existent_user:
        raise ValidationError(error_message)


def validate_username_chars(username):
    if not username.isalnum():
        raise ValidationError(
            _('Username "%(username)s" cannot contain invalid characters'),
              code='invalid_chars_username',
            params={'username': username},
        )
