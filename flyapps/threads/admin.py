from django.contrib import admin
from .models import Thread, Post, ThreadLikeDislike


class PostStackedInline(admin.StackedInline):
    model = Post
    extra = 5


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'category', 'starter', 'prefix', 'pin', 'created', 'modified', 'is_hidden', 'is_locked']
    list_filter = ['category', 'starter', 'is_hidden', 'is_locked', 'prefix', 'pin']
    search_fields = ['title', 'content', 'category']
    date_hierarchy = 'created'
    ordering = ['title', 'starter', 'pin', 'category', 'is_hidden', 'is_locked', 'created', 'modified', 'prefix']
    inlines = [PostStackedInline]

@admin.register(ThreadLikeDislike)
class ThreadAdminLikeDislike(admin.ModelAdmin):
    list_display = ['thread', 'user', 'value']
    list_filter = ['thread']
    search_fields = ['thread', 'user']
    ordering = ['thread', 'user']