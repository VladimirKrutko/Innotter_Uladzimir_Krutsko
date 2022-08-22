from rest_framework.permissions import BasePermission


class UserUpdatePermission(BasePermission):
    """
    Class with manager permission
    """

    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email or request.user.role in ['admin', 'moderator']:
            return True
        return False
