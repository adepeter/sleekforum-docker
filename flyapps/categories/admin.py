from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'id', 'slug', 'description', 'parent']
    search_fields = ['name', 'description', 'parent']
    prepopulated_fields = {
        'slug': ('name',)
    }
    mptt_level_indent = 20