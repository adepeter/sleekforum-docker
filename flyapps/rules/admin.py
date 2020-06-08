from django.contrib import admin
from .models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['category', 'creator', 'name', 'show', 'description']
    list_filter = ['creator', 'category', 'show']
    search_fields = ['name', 'category']
    ordering = ['name', 'category', 'show', 'creator']
