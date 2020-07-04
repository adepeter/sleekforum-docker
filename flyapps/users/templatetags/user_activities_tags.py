from django import template
from django.db.models import Q

from ...categories.models import Category

register = template.Library()

@register.simple_tag(name='categories')
def user_categories(user_obj):
    user_posts = user_obj.post_set.all()
    user_threads = user_obj.threads.all()
    queryset = Q(threads__in=user_threads) | Q(threads__posts__in=user_posts)
    categories = Category.objects.filter(queryset).distinct()
    print(categories)
    return categories