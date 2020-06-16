from django.contrib import admin

from ..miscs.utils.text import truncator

from .models import Message, Reply


class ReplyAdminInline(admin.StackedInline):
    model = Reply
    extra = 3


# @admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'starter',
        'recipient',
        'short_message',
        'message_flag',
        'created',
        'is_replied',
        'modified'
    ]
    inlines = [ReplyAdminInline]

    def short_message(self, obj):
        return truncator(obj.text)

    short_message.description = 'Message preview'

    def message_flag(self, obj):
        return obj.get_flag_display()
    message_flag.short_description = 'State'


# @admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['message', 'sender', 'text', 'created', 'modified']

    def short_message(self, obj):
        return truncator(obj.text)

    short_message.description = 'Reply preview'
