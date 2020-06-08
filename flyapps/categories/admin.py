from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'id', 'slug', 'description', 'parent']
    search_fields = ['name', 'description', 'parent']
    prepopulated_fields = {
        'slug': ('name',)
    }
    save_on_top = True
    mptt_level_indent = 20