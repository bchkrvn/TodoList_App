from django.contrib import admin
from .models import Category, Goal, Comment, Board, BoardParticipant


class GoalInline(admin.TabularInline):
    model = Goal
    fields = ('title', 'priority', 'status', 'due_date', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'title', 'due_date')
    ordering = ('-priority', 'status')
    show_change_link = True
    extra = 0
    can_delete = False


class BoardParticipantInline(admin.TabularInline):
    model = BoardParticipant
    fields = ('user', 'role', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'user')
    ordering = ('role', 'created')
    show_change_link = True
    extra = 0
    can_delete = False


class CategoriesInline(admin.TabularInline):
    model = Category
    fields = ('title', 'user', 'created', 'updated', 'is_deleted')
    readonly_fields = ('created', 'updated', 'user', 'title')
    ordering = ('is_deleted', 'title')
    show_change_link = True
    extra = 0
    can_delete = False


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)
    list_editable = ('is_deleted',)
    readonly_fields = ('created', 'updated')
    inlines = [BoardParticipantInline, CategoriesInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted', 'created', 'updated', 'board')
    search_fields = ('title',)
    list_filter = ('is_deleted', 'user', 'board')
    list_editable = ('is_deleted',)
    readonly_fields = ('created', 'updated', 'user', 'board')
    ordering = ('is_deleted', 'title')
    inlines = [GoalInline]


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('user', 'text', 'created', 'updated')
    readonly_fields = ('created', 'updated', 'user', 'text')
    can_delete = False
    show_change_link = True
    extra = 0


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'priority', 'due_date')
    list_filter = ('category', 'status', 'priority', 'user')
    search_fields = ('title', 'description')
    list_editable = ('status', 'priority')
    readonly_fields = ('created', 'updated', 'user')
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'text', 'created', 'updated')
    search_fields = ('text',)
    readonly_fields = ('created', 'updated', 'user', 'goal')
