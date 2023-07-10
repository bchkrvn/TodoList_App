from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import BoardParticipant


class IsOwner(BasePermission):
    message = 'You are not the owner'

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True


class BoardPermissions(BasePermission):
    message = 'You don\'t have permission to edit this board'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner).exists()
