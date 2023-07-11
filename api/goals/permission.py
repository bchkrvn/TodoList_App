from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import BoardParticipant, Category, Goal, Comment


class BoardPermissions(BasePermission):
    message = "You don't have permission to edit this board"

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner).exists()


class CategoryPermissions(BasePermission):
    message = "You don't have permission to edit this category"

    def has_object_permission(self, request, view, obj: Category):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board).exclude(role=BoardParticipant.Role.reader).exists()


class CreateCategoryPermissions(BasePermission):
    message = "You don't have permission to create this category"

    def has_permission(self, request, view):
        board_id = request.data.get('board')
        return BoardParticipant.objects.filter(
            user=request.user, board_id=board_id).exclude(role=BoardParticipant.Role.reader).exists()


class GoalPermissions(BasePermission):
    message = "You don't have permission to edit this goal"

    def has_object_permission(self, request, view, obj: Goal):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board=obj.category.board).exclude(role=BoardParticipant.Role.reader).exists()


class CreateGoalPermissions(BasePermission):
    message = "You don't have permission to create this goal"

    def has_permission(self, request, view):
        category_id = request.data.get('category')
        return BoardParticipant.objects.filter(
            user=request.user, board__categories__id=category_id).exclude(role=BoardParticipant.Role.reader).exists()


class CommentPermissions(BasePermission):
    message = "You don't have permission to edit this goal"

    def has_object_permission(self, request, view, obj: Comment):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.goal.category.board).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board=obj.goal.category.board).exclude(
            role=BoardParticipant.Role.reader).exists() or obj.user == request.user


class CreateCommentPermissions(BasePermission):
    message = "You don't have permission to create this goal"

    def has_permission(self, request, view):
        goal_id = request.data.get('goal')
        goal = get_object_or_404(Goal, id=goal_id)
        return BoardParticipant.objects.filter(
            user=request.user, board=goal.category.board).exists()
