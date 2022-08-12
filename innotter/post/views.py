from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from post.serializers import PostSerialize
from post.permissions import PostUpdateDeletePermission
from rest_framework.permissions import IsAuthenticated
from post.models import Post
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from page.models import Page


class PostCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerialize

    def post(self, request):

        data = request.data
        print(data)
        # page = Page.objects.get(owner=data['page_id'])
        # data['page_id'] = page

        serializer = self.serializer_class(data=data)
        serializer.is_valid()
        print(serializer.errors)
        serializer.save()
        return Response(serializer.data)


class UpdatePostView(UpdateAPIView):
    pass



class PostUpdateView(UpdateAPIView):
    serializer_class = PostSerialize
    # permission_classes = (PostUpdateDeletePermission,)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        instance = get_object_or_404(Post.objects.all(), id=pk)
        serializer = PostSerialize(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer)
