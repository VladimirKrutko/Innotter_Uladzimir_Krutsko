from rest_framework.permissions import BasePermission


class PostUpdateDeletePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user.role in ['admin', 'moderator']:
            return True

        return False
