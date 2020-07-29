from django.contrib import admin
from django.db import ProgrammingError

from .models import BaseConfiguration


# Register your models here.

class BaseConfigurationAdminMenuMixin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        try:
            BaseConfiguration.load().save()
        except ProgrammingError:
            pass

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
