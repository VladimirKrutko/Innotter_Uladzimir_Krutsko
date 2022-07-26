from .serializers import PageSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Page


class PageUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class UpdatePageView(UpdateAPIView):

    serializer_class = PageSerializer
    permission_classes = (PageUpdatePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        saved_page = get_object_or_404()
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        return Response(data, status.HTTP_200_OK)
