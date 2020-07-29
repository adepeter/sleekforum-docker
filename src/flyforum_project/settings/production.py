from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SLEEKFORUM_DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('SLEEKFORUM_DB_NAME', 'sleekforum_db'),
        'USER': os.environ.get('SLEEKFORUM_DB_USER', 'sleekforum_user'),
        'PASSWORD': os.environ.get('SLEEKFORUM_DB_PASSWORD', 'sleekforum_pass'),
        'HOST': os.environ.get('SLEEKFORUM_DB_HOST', 'localhost'),
        'PORT': os.environ.get('SLEEKFORUM_DB_PORT', '5432')
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
