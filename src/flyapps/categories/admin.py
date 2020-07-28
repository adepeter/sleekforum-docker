from django.contrib import admin, messages
from django.utils.translation import (
    ngettext,
    gettext_lazy as _
)

from mptt.admin import MPTTModelAdmin

from .models import Category


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    actions = ['lock_section', 'unlock_section']
    list_display = [
        'name',
        'id',
        'slug',
        'is_lock',
        'description',
        'parent'
    ]
    search_fields = ['name', 'description', 'parent']
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_filter = [
        'parent',
        'is_lock',
    ]
    save_on_top = True
    mptt_level_indent = 20

    def lock_section(self, request, queryset):
        queryset.update(is_lock=True)
        message = ngettext(
            _('Category successfully locked'),
            _('Categories successfully locked'),
            queryset.count()
        )
        messages.success(request, '%(message)s' % {'message': message})

    lock_section.short_description = _('Lock selected')

    def unlock_section(self, request, queryset):
        queryset.update(is_lock=False)
        message = ngettext(
            _('Category successfully unlocked'),
            _('Categories successfully unlocked'),
            queryset.count()
        )
        messages.success(request, '%(message)s' % {'message': message})

    unlock_section.short_description = _('Unlock selected')