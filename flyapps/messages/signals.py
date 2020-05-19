from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import Message, Reply

message_view_handler = Signal(providing_args=['request'])


@receiver(post_save, sender=Reply)
def is_replied_updater(sender, instance, created, **kwargs):
    if created:
        instance.message.flag = Message.FLAG_NEW
        instance.message.is_replied = True
        instance.message.save(update_fields=['flag', 'is_replied'])

@receiver(message_view_handler)
def read_message_handle(sender, **kwargs):
    """
    This signal handles message flag status so that a message can be flagged as
    either:
        1. New message
        2. New reply.
        3. Active conversation
    The comment code blocks and the uncomment one serves same purpose (view source for code).
    """

    message = kwargs.get('obj')
    current_user = kwargs.get('request')
    message_viewers = [message_viewers.user for message_viewers in message.message_views.all()]
    if not current_user in message_viewers:
        message.message_views.create(user=current_user)
        message.flag = Message.FLAG_ACTIVE
    else:
        if message.flag == Message.FLAG_NEW:
            message.flag = Message.FLAG_ACTIVE
    message.save(update_fields=['flag'])
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # if message.replies.exists():
    #     users = User.objects.filter(message_views__in=message.message_views.all())
    #     if current_user in users and message.flag == Message.FLAG_NEW:
    #         message.flag = Message.FLAG_ACTIVE
    #     else:
    #         message.message_views.create(user=current_user)
    #         message.flag = Message.FLAG_ACTIVE
    #     message.save(update_fields=['flag'])