from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ..managers.user import UserManager

GENDER = (
    ('m', 'Male'),
    ('f', 'Female'),
)


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name=_('e-mail'), unique=True)
    username = models.CharField(verbose_name=_('username'), max_length=25, unique=True)
    slug = models.SlugField(verbose_name=_('username slug'), blank=True)
    avatar = models.ImageField(upload_to='images', blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=1, choices=GENDER, blank=True)
    dob = models.DateField(blank=True, null=True)
    about = models.TextField(verbose_name=_('About me'), blank=True)
    location = models.CharField(max_length=75, blank=True)
    signature = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    phone_number = models.PositiveIntegerField(default=0)
    website = models.URLField(default='https://', blank=True)
    github = models.URLField(default='https://github.com/', blank=True)
    facebook = models.URLField(default='https://facebook.com/', blank=True)
    twitter = models.URLField(default='https://twitter.com/@', blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email_on_user'),
            models.UniqueConstraint(fields=['username'], name='unique_username_on_user'),
            models.UniqueConstraint(fields=['email', 'slug'], name='unique_email_slug_on_user')
        ]
        indexes = [
            models.Index(fields=['slug'], name='index_slug_on_user'),
            models.Index(fields=['id', 'slug'], name='index_id_slug_on_user')
        ]
        ordering = ['email']

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.title()

    def get_short_name(self):
        return self.username

    @property
    def get_display_name(self):
        if self.first_name or self.last_name:
            return self.get_full_name().rstrip()
        return self.username

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }
        return reverse('flyapps:users:profile:user_profile', kwargs=kwargs)

    def __str__(self):
        return '%s - %s' % (self.username, self.email)
