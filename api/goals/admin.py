from django.contrib import admin
from .models import Category, Goal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)
    list_editable = ('is_deleted',)
    readonly_fields = ('created', 'updated')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'priority', 'due_date')
    list_filter = ('category', 'status', 'priority', 'user')
    search_fields = ('title', 'description')
    list_editable = ('status', 'priority')
    readonly_fields = ('created', 'updated')
