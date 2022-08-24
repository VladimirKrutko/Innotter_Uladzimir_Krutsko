from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from post.serializers import PostCreateSerializer
from post.permissions import PostUpdatePermission, PostDeletePermission
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from user.models import User
# from post.tasks import send_email


class PostAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated, PostUpdatePermission)
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['page_id'] = User.objects.get(email=request.user.email).pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = Post.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request, obj=instance)
        data['page_id'] = kwargs['pk']
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)

    def put_like(self, request, *args, **kwargs):
        data = request.data
        instance = Post.objects.get(pk=kwargs['pk'])
        data['page_id'] = kwargs['pk']
        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)


class PostDeleteView(UpdateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = (PostDeletePermission, IsAuthenticated)

    def put(self, request, *args, **kwargs):
        instance = Post.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request, obj=instance)

        data = request.data
        if len(data.keys()) > 1:
            raise APIException('Incorrect number of fields. Only is_delete field')

        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data)
