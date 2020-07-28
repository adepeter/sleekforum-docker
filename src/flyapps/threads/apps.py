from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ThreadsConfig(AppConfig):
    name = 'flyapps.threads'
    verbose_name = _('Thread')

    def ready(self):
        from . import signals
