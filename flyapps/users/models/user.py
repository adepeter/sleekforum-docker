from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from ..managers.user import UserManager

GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('e-mail'), unique=True)
    username = models.CharField(verbose_name=_('username'), max_length=25, unique=True)
    username_slug = models.SlugField(verbose_name=_('username slug'), blank=True, db_index=True)
    avatar = models.ImageField(upload_to='images', blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=1, choices=GENDER, blank=True)
    dob = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=75, blank=True)
    signature = models.TextField(blank=True)
    threads = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    is_hide_presence = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    phone_number = models.PositiveIntegerField(default=0)
    website = models.URLField(default='https://', blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'username_slug'], name='unique_user')
        ]
        ordering = ['email']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.title()

    def get_short_name(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username_slug = slugify(self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.username, self.email)
