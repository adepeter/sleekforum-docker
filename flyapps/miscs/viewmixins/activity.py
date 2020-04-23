from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, FieldDoesNotExist
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin


class BaseActivityActionMixin(SingleObjectMixin):
    activity_model = None
    activity_field_name = 'action_value'
    activity_exclusion = False
    excluded_activity_actions = ['LIK', 'DSL', 'FAV']
    activity_action = None

    def get_user_activity_object(self, activity_queryset=None):
        """ This method is used to get user single activity"""
        # It's similar in function to get_object() of SingleObjectMixin
        if activity_queryset is None:
            activity_queryset = self.get_activity_queryset_for_object(self.object)
        if self.activity_exclusion is True:
            if self.excluded_activity_actions:
                activity_field_name = self.get_activity_field_name()
                activity_queryset = activity_queryset.exclude(**{
                    activity_field_name + str('__in'): self.excluded_activity_actions
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

    def get_activity_queryset_for_object(self, obj):
        activity_model = self.get_activity_model()
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
        self.activity_model = self.get_activity_model()
        self.object = self.get_object()
        self.existing_actions = self.get_activity_queryset_for_object(self.object)
        self.field_name = self.get_activity_field_name()
        try:
            field_name = self.field_name
            get_user_activity_action = self.get_user_activity_object(self.existing_actions)
            if getattr(get_user_activity_action, field_name) != self.activity_action:
                setattr(get_user_activity_action, field_name, self.activity_action)
                get_user_activity_action.save(update_fields=[field_name])
                print('Updating activity_action')
            else:
                get_user_activity_action.delete()
                print('deleting activity_action')
        except self.activity_model.DoesNotExist:
            print('Creating activity_action')
            create_action = {
                'user': self.request.user,
                'content_object': self.object,
                self.field_name: self.activity_action,
            }
            self.activity_model.objects.create(**create_action)
        return self.get_success_url()

    def get_success_url(self):
        if self.success_url:
            return HttpResponseRedirect(str(self.success_url))
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
