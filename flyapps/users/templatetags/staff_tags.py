from django import template
from django.contrib.auth import get_user_model

User = get_user_model()

register = template.Library()


def get_user(**kwargs):
    qs = User.objects.filter(is_active=True, **kwargs)
    if kwargs.get('groups'):
        groups = kwargs['groups'].split(',')
        return qs.filter(groups__in=groups)
    return qs


@register.simple_tag(name='staffs')
def get_staffs(**kwargs):
    kwargs.setdefault('is_staff', True)
    return get_user(**kwargs)


@register.simple_tag(name='superusers')
def get_superusers(**kwargs):
    kwargs.setdefault('is_superuser', True)
    return get_staffs(**kwargs)
