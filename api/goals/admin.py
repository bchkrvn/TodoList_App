from django.contrib import admin
from .models import Category


@admin.register(Category)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted', 'created', 'updated')
    list_filter = ('is_deleted',)
    list_editable = ('is_deleted',)
    readonly_fields = ('created', 'updated')
