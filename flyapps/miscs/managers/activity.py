from django.contrib.contenttypes.models import ContentType
from django.db import models


class ActivityManager(models.Manager):

    def filter_action_by(self, action_value, obj=None):
        if obj is not None:
            return self.filter(
                content_type=ContentType.objects.get_for_model(obj),
                action_value__iexact=action_value,
                object_id=obj.id
            )
        return self.filter(action_value=action_value)