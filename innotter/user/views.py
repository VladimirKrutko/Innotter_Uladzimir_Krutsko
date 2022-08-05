from rest_framework import status
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError

from user.serializers import LoginSerializer, UserRegistration, UpdateUserSerializer
from user.renderers import UserJSONRenderer


class ManagerPermission(BasePermission):
    """
    Class with manager permission
    """

    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if (obj.author != request.user) and (request.user.role == 'moderator'):
            return True
        return False


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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    Class that realize log in operation for user
    """
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        print('user', user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = (UpdateUserSerializer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            raise ValidationError('Something go wrong')
        return Response(serializer.data, status=status.HTTP_200_OK)
