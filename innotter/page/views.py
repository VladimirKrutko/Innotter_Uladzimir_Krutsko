from .serializers import \
    (PageSerializer, PagePublicSerializer, PagePrivateSerializer, BlockPageSerializer)
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from page.models import Page
from page.permissions import PagePermission, PageBlockPermissions, PageShowPermissions
from post.models import Post


class UpdatePageView(UpdateAPIView):
    serializer_class = PageSerializer
    permission_classes = [PagePermission]

    def put(self, request, *args, **kwargs):

        instance = Page.objects.get(id=kwargs['pk'])
        self.check_object_permissions(request, instance)
        data = request.data
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(data)


class BlockPageView(UpdatePageView):
    serializer_class = BlockPageSerializer
    permission_classes = [PageBlockPermissions]

    def put(self, request, *args, **kwargs):
        instance = Page.objects.get(id=kwargs['pk'])
        data = request.data
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data)


class AddFollowersPublicPage(UpdatePageView):
    serializer_class = PagePublicSerializer
    permission_classes = (PagePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):

        instance = get_object_or_404(Page.objects.all(), pk=int(kwargs['pk']))
        self.check_object_permissions(request=request, obj=instance)
        data = request.data
        serializer = self.serializer_class(data={'followers': data.get('followers')}, instance=instance)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        serializer.save()

        return Response()


class AddFollowersPrivatePage(UpdatePageView):
    serializer_class = PagePrivateSerializer
    permission_classes = (PagePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        instance = get_object_or_404(Page.objects.all(), id=kwargs['pk'])
        self.check_object_permissions(request=request, obj=instance)
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


class ListPagePostView(ListAPIView):
    permission_classes = (PageShowPermissions,)

    def get(self, request, *args, **kwargs):
        page_id = kwargs['pk']
        page = Page.objects.get(pk=page_id)
        self.check_object_permissions(request=request, obj=page)

        post = Post.objects.get(page_id=page_id)
        response_json = PageSerializer.serialize_page_post(page_obj=page, post_obj=post)

        return Response(response_json)


class ListFollowRequestView(ListPagePostView):
    permission_classes = (PagePermission,)

    def get(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request, obj=page)
        page_json = serializers.serialize('json', [page,])
        response_json = {'follow_request': page_json['follow_requests']}
        return Response(response_json)
