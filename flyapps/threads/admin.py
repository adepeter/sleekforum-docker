from django.contrib import admin
from .models import Thread, Post, ThreadParticipant, ThreadView, ThreadEdit


# Register your models here.

class PostStackedInline(admin.StackedInline):
    model = Post
    extra = 5


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'category', 'starter', 'slug', 'prefix', 'created', 'modified', 'is_hidden', 'is_locked']
    list_filter = ['category', 'starter', 'is_hidden', 'is_locked', 'prefix']
    search_fields = ['title', 'content', 'category']
    date_hierarchy = 'created'
    ordering = ['title', 'starter', 'category', 'is_hidden', 'is_locked', 'created', 'modified', 'prefix']
    inlines = [PostStackedInline]


admin.site.register(Post)
admin.site.register(ThreadParticipant)
admin.site.register(ThreadEdit)
admin.site.register(ThreadView)
