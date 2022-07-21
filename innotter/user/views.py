from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import User
from rest_framework.serializers import ValidationError
from user.serializers import LoginSerializer, UserSerializer
from .renderers import UserJSONRenderer
from django.conf import settings


class UserAPIView(ModelViewSet):
    """
    Class that realize functionality for register new user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        """
        Realize user registration
        Args:
            request (json): requset with user data for registration

        Returns:
            user data , status code 
        """
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):

        data = request.data.get('user')
        try:
            instance = User.objects.get(email=data['email'])
        except:
            raise ValidationError('please input email')

        serializer = self.serializer_class(data=data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """
    Class that realize log in operation for user
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadImageAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    renderer_classes = None

    def post(self, request, format=None):
        """
        _summary_

        Args:
            request (_type_): _description_
        """
        serializer = ImageSerializer(data=request.data)

        image = serializer.data['image']
        file_name = request.data.get('name')
        image_link = settings.AWS_BASE_STORAGE + '/user-image/' + file_name
        settings.S3_BUCKET.put_object(Key=image_link, Body=image)
        return Response(image_link, status=status.HTTP_200_OK)
