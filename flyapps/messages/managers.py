from django.db import models

class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter()