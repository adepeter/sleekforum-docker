from django.contrib import admin

from .models import Message, Reply


# Register your models here.
def truncator(obj, word_count=20, completer='...'):
    splitted_text = obj.split()
    if len(splitted_text) > word_count:
        obj = ' '.join((splitted_text)[:word_count]).rstrip()
        return '{0} {1}'.format(obj, completer)
    return obj


class ReplyAdminInline(admin.StackedInline):
    model = Reply
    extra = 3


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['starter', 'recipient', 'short_message', 'created', 'is_replied', 'modified']
    inlines = [ReplyAdminInline]

    def short_message(self, obj):
        text = obj.text
        return truncator(text)

    short_message.description = 'Message preview'


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['message', 'sender', 'text', 'created', 'modified']

    def short_message(self, obj):
        text = obj.text
        return truncator(text)

    short_message.description = 'Reply preview'
