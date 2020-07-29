from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('E-mail field cannot be empty'))
        if not username:
            raise ValueError(_('Username field cannot be empty'))
        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
            password=self.make_random_password() if password is None else password,
            **extra_fields
        )
        user.slug = slugify(username)
        user.set_password(password)
        now = timezone.now()
        user.date_created = now
        user.last_login = now
        user.last_modified = now
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Please set 'is_staff' as True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Please set 'is_superuser' as True"))
        return self._create_user(email, username, password, **extra_fields)

    def get_by_username_or_email(self, login):
        if '@' in login:
            return self.get(email__iexact=login)
        return self.get(slug__iexact=login)