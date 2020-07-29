from django.core.mail import mail_admins
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models.report import Violation


@receiver(post_save, sender=Violation)
def pm_admins_for_action(sender, instance, created, **kwargs):
    subject = 'Report for violation'
    message = instance
    if created:
        mail_admins(subject, message)
