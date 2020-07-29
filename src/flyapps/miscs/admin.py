from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Action, Violation


# Register your models here.

class ActivityStackedInline(GenericStackedInline):
    model = Action
    extra = 5


@admin.register(Action)
class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'action_value',
        'object_id',
        'content_type',
        'content_object'
    ]


@admin.register(Violation)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'is_violated',
        'reported_on',
        'object_id',
        'content_type',
        'content_object'
    ]
    list_filter = ['user', 'rules', 'content_type', 'is_violated']
    ordering = ['user', 'rules']
