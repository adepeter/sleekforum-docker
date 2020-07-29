from django.db.models import F
from django.dispatch import receiver, Signal
from django.db.models.signals import post_save

from ..miscs.models.activity import Action
from ..miscs.signals.activity import activity_updater

from .models.thread import Thread

thread_views_creator_and_updater = Signal(providing_args=['request', 'thread'])


@receiver(post_save, sender=Thread)
def handle_thread_view_creation(sender, instance, created, **kwargs):
    """
    Create new thread view and add a new counter.
    Although this signal has a limitation as you cant plug it in view.
    To fix this limitation, a custom signal was created
    """
    if created:
        instance.views = F('views') + 1
        instance.save(update_fields=['views'])
        instance.thread_views.create(user=instance.starter)


@receiver(thread_views_creator_and_updater)
def handle_thread_views(sender, request, **kwargs):
    """
    Does everything handle_thread_view_creation() signal cannot do
    Implement this signal in any where of your site
    """

    # Yet to be implemented
    if request.user.is_authenticated:
        print(sender)


@receiver(post_save, sender=Action)
def like_and_dislike_handler(sender, instance, created, **kwargs):
    from django.contrib.contenttypes.models import ContentType
    ct = ContentType.objects.get_for_model(instance).get_object_for_this_type()
    if created:
        get_ct_for_obj_of_instance = instance.content_object
        if instance.action_value == Action.LIKE:
            get_ct_for_obj_of_instance.likes = ct
            print('Ading likes counter')
        else:
            print('Adding dislike counter')
            get_ct_for_obj_of_instance.dislikes = ct
        get_ct_for_obj_of_instance.save()


# @receiver(activity_updater)
# def hal(sender, **kwargs):
#     print('Sender is', sender, kwargs.get('obj'))
