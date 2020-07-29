"""
WSGI config for flyforum project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
flyforum_env = os.environ.get('SETTINGS_ENV', 'flyforum_project.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', flyforum_env)

application = get_wsgi_application()
