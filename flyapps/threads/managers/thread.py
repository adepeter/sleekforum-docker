from django.db import models


class ThreadManager(models.Manager):
    def unhidden_threads(self, **kwargs):
        return self.filter(is_hidden=False, **kwargs)

    def hidden_threads(self, **kwargs):
        return self.filter(is_hidden=True, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-pin', '-modified')


class ThreadParticipantManager(models.Manager):
    pass
