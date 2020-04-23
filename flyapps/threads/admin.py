from django.contrib import admin

from ..miscs.admin import ActivityStackedInline
from .models import Thread, Post


class PostStackedInline(admin.StackedInline):
    model = Post
    extra = 5


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'category', 'starter', 'prefix', 'pin', 'created', 'modified', 'is_hidden', 'is_locked']
    list_filter = ['category', 'starter', 'is_hidden', 'is_locked', 'prefix', 'pin']
    search_fields = ['title', 'content', 'category']
    radio_fields = {
        'pin': admin.HORIZONTAL,
        'prefix': admin.HORIZONTAL,
    }
    date_hierarchy = 'created'
    ordering = ['title', 'starter', 'pin', 'category', 'is_hidden', 'is_locked', 'created', 'modified', 'prefix']
    inlines = [ActivityStackedInline, PostStackedInline]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'thread', 'parent', 'content', 'is_hidden', 'created', 'modified']
    search_fields = ['content', 'user', 'thread', 'parent']
    list_filter = ['user', 'thread', 'parent', 'is_hidden']
    date_hierarchy = 'created'