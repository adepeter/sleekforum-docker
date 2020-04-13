from django.db import models


class ThreadManager(models.Manager):
    def unhidden_threads(self):
        return self.filter(is_hidden=False)

    def hidden_threads(self):
        return self.filter(is_hidden=True)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-pin', 'modified')


class ThreadParticipantManager(models.Manager):
    pass
