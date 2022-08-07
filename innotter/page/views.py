from .serializers import PageSerializer, PagePublicSerializer, PagePrivateSerializer
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

        instance = get_object_or_404(Page.objects.all(), id=kwargs['pk'])
        data = request.data
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(data, status.HTTP_200_OK)


class AddFollowersPublicPage(UpdatePageView):
    serializer_class = PagePublicSerializer
    permission_classes = (PageUpdatePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(Page.objects.all(), id=kwargs['pk'])
        data = request.data
        serializer = self.serializer_class(data=data, instance=instance)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return serializer.errors

        serializer.save()

        return Response(serializer, status.HTTP_200_OK)


class AddFollowersPrivatePage(UpdatePageView):
    serializer_class = PagePrivateSerializer
    permission_classes = (PageUpdatePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(Page.objects.all(), id=kwargs['pk'])
        data = request.data
        serializer = self.serializer_class(data=data, instance=instance)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return serializer.errors

        serializer.save()

        return Response(serializer, status.HTTP_200_OK)






