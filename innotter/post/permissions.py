from rest_framework.permissions import BasePermission
from user.models import User


class PostUpdatePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.page_id.owner == request.user:
            return True

        return False


class PostDeletePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = User.objects.get(email=request.user)
        if obj.page_id.owner == request.user or user.role in ['admin', 'moderator']:
            return True

        return False
