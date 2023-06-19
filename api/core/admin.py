from django.contrib import admin

from .forms import UserFormAdmin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', ]
    list_filter = ['is_staff', 'is_active']
    list_editable = ['is_staff', 'is_active']
    form = UserFormAdmin
