from rest_framework.viewsets import ViewSet
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from post.serializers import PostSerialize
from rest_framework.decorators import action
from post.permissions import PostUpdatePermission
from post.models import Post


class PostCreateView(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerialize

    @action(detail=True, methods=['post'])
    def create(self, request):
        data = request.data.get('post_info')
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer


class PostUpdateView(UpdateAPIView):
    serializer_class = PostSerialize
    queryset = Post.objects.all()
    permission_classes = (PostUpdatePermission,)


class PostCRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerialize
    queryset = Post.objects.all()

class PostDeleteView():
    pass




