from django import template

from ..models.activity import Action

register = template.Library()

@register.simple_tag
def activity_action_queryset(action_value, obj):
    return Action.objects.filter_action_by(action_value, obj)