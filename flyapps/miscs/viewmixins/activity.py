from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, FieldDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

class BaseActivityActionMixin(SingleObjectMixin):
    activity_model = None
    activity_field_name = ''
    field_exclusion = False
    excluded_fields = []
    activity_action = None

    """ This method is used to get user single activity"""
    # It's similar in function to get_object() of SingleObjectMixin
    def get_user_activity_object(self, activity_queryset=None):
        if activity_queryset is None:
            activity_queryset = self.fetch_activity_queryset()
        if self.field_exclusion is True:
            if self.excluded_fields:
                activity_field_name = self.get_activity_field_name()
                activity_queryset = activity_queryset.exclude(**{
                    activity_field_name + str('__in'): self.excluded_fields
                })
            else:
                raise AttributeError('You cant set field_exclusion to True and excluded_fields as empty')
        return activity_queryset.get(user=self.request.user)

    def get_activity_field_name(self):
        if not self.activity_field_name or self.activity_field_name is None:
            raise ImproperlyConfigured('activity_field_name attrs for this view is missing')
        return self.validate_activity_field_name(self.activity_field_name)

    def validate_activity_field_name(self, field_name):
        if self.activity_model is not None:
            fields = [field.name for field in self.activity_model._meta.get_fields()]
            if field_name not in fields:
                raise FieldDoesNotExist(
                    '%(field_name)s does not seem to be a valid field name on %(activity_model)s' % {
                        'field_name': field_name,
                        'activity_model': self.activity_model._meta.object_name
                    })
            else:
                return field_name
        else:
            raise ImproperlyConfigured('to validate field, you must set activity_model attrs')

    def fetch_activity_queryset(self, obj=None):
        activity_model = self.get_activity_model()
        if obj is None:
            obj = self.get_object()
        return activity_model.objects.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id
        )

    def get_activity_model(self):
        if self.activity_model is None:
            raise ImproperlyConfigured('You must set activity_model attrs on this view')
        return self.activity_model


class BaseActivityActionView(BaseActivityActionMixin, View):
    success_url = ''

    def get(self, request, *args, **kwargs):
        self.field = self.get_activity_field_name()
        self.activity_model = self.get_activity_model()
        self.object = self.get_object()
        self.existing_actions = self.fetch_activity_queryset(self.object)
        try:
            field_name = self.get_activity_field_name()
            get_user_upvote = self.get_user_activity_object(self.existing_actions)
            if getattr(get_user_upvote, field_name) != self.activity_action:
                setattr(get_user_upvote, field_name, self.activity_action)
                get_user_upvote.save(update_fields=[field_name])
                print('Updating upvote')
            else:
                get_user_upvote.delete()
                print('deleting upvotes')
        except self.activity_model.DoesNotExist:
            print('Creating upvote')
            create_action = {
                'user': self.request.user,
                'content_object': self.object,
                self.field: self.activity_action,
            }
            self.activity_model.objects.create(**create_action)
        return self.get_success_url()

    def get_success_url(self):
        if self.success_url:
            return HttpResponseRedirect(str(self.success_url))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))