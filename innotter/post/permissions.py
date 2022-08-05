from rest_framework.permissions import BasePermission


class PostUpdatePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        else:
            return False
