from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reply


@receiver(post_save, sender=Reply)
def is_replied_updater(sender, instance, created, **kwargs):
    if created:
        instance.message.is_replied = True
        instance.message.save(update_fields=['is_replied'])
