from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'flexapps.users'

    def ready(self):
        from . import signals
