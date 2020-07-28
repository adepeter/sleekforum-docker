from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms.admin import UserAdminCreationForm, UserAdminChangeForm
from .models import Ban, Role

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly = ['username', 'date_created', 'date_modified', 'last_login']
    list_display = ['username', 'email', 'roles', 'date_joined', 'last_seen', 'last_modified']
    radio_fields = {
        'sex': admin.HORIZONTAL
    }
    fieldsets = [
        (None, {
            'fields': [('email', 'username',),],
        }),
        (_('Permissions'), {
            'fields': ['is_staff', 'is_superuser'],
        }),
        (_('Personal Information'), {
            'fields': ['avatar', 'first_name', 'last_name', 'sex',
                       'dob', 'signature', 'about', 'location']
        }),
        (_('Contact Information'), {
            'fields': ['phone_number', 'facebook', 'twitter',
                       'github', 'website']
        }),
    ]
    add_fieldsets = [
        (None, {
            'fields': ['email', 'username'],
        })
    ]
    list_per_page = 20

    def roles(self, obj):
        roles = obj.roles
        if roles.exists():
            return obj.roles.all()
        return 'No role'

    roles.short_description = 'Roles'
    roles.empty_value_display = 'No Role yet'

    def date_joined(self, obj):
        return obj.date_created

    date_joined.short_description = _('Date joined')

    def last_seen(self, obj):
        return obj.last_login

    last_seen.short_description = _('Last seen')

    def last_modified(self, obj):
        return obj.date_modified

    last_modified.short_description = _('Profile last updated')


@admin.register(Role)
class RoleAdmin(GroupAdmin):
    """ HEloo"""


admin.site.unregister(Group)

@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'banned_by',
        'created',
        'modified',
        'expiry',
    ]