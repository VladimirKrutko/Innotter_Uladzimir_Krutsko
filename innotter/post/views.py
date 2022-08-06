from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, RetrieveUpdateDestroyAPIView
from post.serializers import PostSerialize
from post.permissions import PostUpdatePermission
from post.models import Post
from rest_framework.response import Response


class PostCreateView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = PostSerialize

    def post(self, request):

        data = request.data.get('post')
        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)


class PostUpdateView(UpdateAPIView):
    serializer_class = PostSerialize
    permission_classes = (PostUpdatePermission,)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = Post.objects.get(pk=pk)

        serializer = PostSerialize(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer)


class PostCRUDView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerialize
    queryset = Post.objects.all()

class PostDeleteView():
    pass




