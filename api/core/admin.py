from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', ]
    list_filter = ['is_staff', 'is_active']
    list_editable = ['is_staff', 'is_active']
    readonly_fields = ('date_joined', 'last_login')
