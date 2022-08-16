from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import LoginSerializer, UserRegistration, UpdateUserSerializer
from user.renderers import UserJSONRenderer
from user.permissions import UserUpdatePermission
from user.models import User


class RegistrationAPIView(APIView):
    """
    Class that realize functionality for register new user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistration
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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


class UpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, UserUpdatePermission)
    serializer_class = (UpdateUserSerializer,)

    def put(self, request, *args, **kwargs):
        user = request.data
        instance = User.objects.get(email=user['email'])
        self.check_object_permissions(request, user)
        serializer = self.serializer_class(data=user, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
