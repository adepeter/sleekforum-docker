from django import template

from ...threads.models.thread import Thread

register = template.Library()

@register.simple_tag
def category_threads(category, include_self=True):
    return Thread.objects.filter(
        category__in=category.get_descendants(include_self=include_self)
    )
