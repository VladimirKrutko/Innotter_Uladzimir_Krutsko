from rest_framework.permissions import BasePermission
from page.models import Page


class PostUpdateDeletePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        page = Page.objects.get(owner=request.user)
        if obj.page_id.owner == page.owner:
            return True

        return False
