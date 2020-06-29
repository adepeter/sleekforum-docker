from .base import *

DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_secret('DJANGO_DB_ENGINE'),
        'NAME': get_secret('DJANGO_DB_NAME'),
        'USER': get_secret('DJANGO_DB_USER'),
        'PASSWORD': get_secret('DJANGO_DB_PASSWORD'),
        'HOST': get_secret('DJANGO_DB_HOST'),
        'PORT': get_secret('DJANGO_DB_PORT'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
