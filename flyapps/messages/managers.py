from django.db import models
from django.db.models import Count

class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            latest_reply=Count('replies__created')
        ).order_by('-modified', '-latest_reply')