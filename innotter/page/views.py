from .serializers import PageSerializer, PagePublicSerializer, PagePrivateSerializer
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.generics import get_object_or_404
from page.models import Page
from page.permissions import PageUpdatePermission


class UpdatePageView(UpdateAPIView):
    serializer_class = PageSerializer
    permission_classes = (PageUpdatePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        instance = Page.objects.get(id=kwargs['pk'])
        data = request.data
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(data)


class AddFollowersPublicPage(UpdatePageView):
    serializer_class = PagePublicSerializer

    permission_classes = (PageUpdatePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):

        instance = get_object_or_404(Page.objects.all(), pk=int(kwargs['pk']))

        data = request.data
        serializer = self.serializer_class(data={'followers':data.get('followers')}, instance=instance)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        serializer.save()

        return Response()


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

        return Response(serializer)


class ListPagesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PageSerializer
    queryset = Page.objects.all()
