from rest_framework.permissions import BasePermission
from user.models import User


class PagePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner.email == request.user.email:
            return True
        return False


class PageBlockPermissions(BasePermission):

    def has_permission(self, request, view):
        user = User.objects.get(email=request.user)
        if user.role in ['admin', 'moderator']:
            return True
        return False


class PageShowPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not obj.is_private or obj.followers.filter(email=request.user) or request.user.is_admin:
            return True
        else:
            return False
