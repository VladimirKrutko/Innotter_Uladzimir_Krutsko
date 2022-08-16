from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView
from post.serializers import PostSerializer
from post.permissions import PostUpdatePermission, PostDeletePermission
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from rest_framework.response import Response
from rest_framework.exceptions import APIException


class PostAPIView(ModelViewSet):
    permission_classes = (IsAuthenticated, PostUpdatePermission)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['email'] = request.user
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = Post.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request, obj=instance)

        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PostDeleteView(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = (PostDeletePermission,IsAuthenticated)

    def put(self, request, *args, **kwargs):
        instance = Post.objects.get(pk=kwargs['pk'])
        self.check_object_permissions(request=request, obj=instance)

        data = request.data
        if data.keys() > 1:
            raise APIException('Incorrect number of fields. Only is_delete field')

        serializer = self.serializer_class()
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)



