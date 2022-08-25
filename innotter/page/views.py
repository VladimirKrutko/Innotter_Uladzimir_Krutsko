from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from django.core import serializers
from django.core import serializers as dj_ser
from django.db.models import Q

from page.models import Page
from user.models import User
from page.permissions import PagePermission, PageBlockPermissions, PageShowPermissions
from post.models import Post
from page.serializers import PageSerializer, PagePublicSerializer, PagePrivateSerializer

import json


class PageViewSet(ViewSet):
    """
    Class has method for:
        1. Update page by user - update_by_user()
        2. Add followers for public page - add_follower_public()
        3. Add followers for private page - add_follower_private()
        4. Get all pages - get_all_pages()
        5. Search pages by uuid, name, username - search_object()
        6. Get user follow requests - get_follow_requests()
    """

    permission_classes = (PagePermission, IsAuthenticated)
    serializer_class = {
        'page_serializer': PageSerializer,
        'page_public_foll': PagePublicSerializer,
        'page_private_foll': PagePrivateSerializer,
    }

    def update_by_user(self, request, *args, **kwargs):
        ser_class = self.serializer_class['page_serializer']
        instance = Page.objects.get(id=kwargs['pk'])
        self.check_object_permissions(request, instance)
        data = request.data

        serializer = ser_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(data=serializer.data, status=HTTP_200_OK)

    def add_follower_public(self, request, *args, **kwargs):
        """
        add followers for public page
        """
        ser_class = self.serializer_class['page_public_foll']
        instance = get_object_or_404(Page.objects.all(), pk=int(kwargs['pk']))
        data = request.data
        self.check_object_permissions(request=request, obj=instance)

        serializer = ser_class(data={'followers': data.get('followers')}, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'followers': serializer.data['followers']}, status=HTTP_200_OK)

    def add_follower_private(self, request, *args, **kwargs):
        ser_class = self.serializer_class['page_private_foll']
        instance = get_object_or_404(Page.objects.all(), id=kwargs['pk'])
        data = request.data
        self.check_object_permissions(request=request, obj=instance)

        serializer = ser_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=
        {
            'followers': serializer.data['followers'],
            'follow_requests': serializer['follow_requests']
        },
            status=HTTP_200_OK)

    def _get_filter_qs(self, field_name, filter_value):
        """
        Function that return filter values from query_set by
        filed_value and filter_value
        """
        kwargs = {'{}_iexact'.format(field_name): filter_value}
        return Q(**kwargs)

    def search_object(self, request, *args, **kwargs):
        """
        data -> {model_name: val,
                field_name: val,
                filter_val: val}
        """
        data = request.data
        all_pages = Page.objects.all()
        all_users = User.objects.all()
        filter_objects = Q()

        if data.get('model_name') == 'page':
            filter_objects &= self._get_filter_qs(field_name=data['field_name'], filter_value=data['filter_val'])
            filter_data = all_pages.filter(filter_objects)
            json_result = json.loads(dj_ser.serialize('json', filter_data))
            return Response(data=json_result, status=HTTP_200_OK)

        elif data.get('model_name') == 'page':
            filter_objects &= self._get_filter_qs(field_name=data['field_name'], filter_value=data['filter_val'])
            filter_data = all_users.filter(filter_objects)
            json_result = json.loads(dj_ser.serialize('json', filter_data))
            return Response(data=json_result, status=HTTP_200_OK)

        return Response(data={'result': 'Not_found'}, status=HTTP_200_OK)

    def get_all_pages(self, request, *args, **kwargs):
        json_page = dj_ser.serialize('json', Page.objects.all())
        return Response(data=json_page, status=HTTP_200_OK)

    def get_follow_requests(self, request, *args, **kwargs):
        page = Page.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request, obj=page)
        page_json = json.loads(serializers.serialize('json', [page, ]))
        response_json = {'follow_request': page_json[0]['fields']['follow_requests']}
        return Response(response_json)


class BlockPageView(UpdateAPIView):
    serializer_class = PageSerializer
    permission_classes = (PageBlockPermissions, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        if len(request.data.keys()) > 2:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            instance = Page.objects.get(id=kwargs['pk'])
            data = request.data
            serializer = self.serializer_class(data=data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data)


class ListPagePostView(ListAPIView):
    permission_classes = (PageShowPermissions,)

    def get(self, request, *args, **kwargs):
        page_id = kwargs['pk']
        page = Page.objects.get(pk=page_id)
        self.check_object_permissions(request=request, obj=page)

        post = Post.objects.filter(page_id=page_id)
        response_json = PageSerializer.serialize_page_post(page_obj=page, post_obj=post)

        return Response(response_json)
