from rest_framework import status
<<<<<<< HEAD
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from user.models import User
from rest_framework.serializers import ValidationError
from user.serializers import LoginSerializer, UserSerializer
from user.renderers import UserJSONRenderer


class UserAPIView(ModelViewSet):
=======
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import LoginSerializer, UserRegistration, UpdateUserSerializer
from user.renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
>>>>>>> _26.07.2022_Working_with_page_model
    """
    Class that realize functionality for register new user
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
<<<<<<< HEAD
        """
        Realize user registration
        Args:
            request (json): request with user data for registration

        Returns:
            user data , status code 
        """
=======
>>>>>>> _26.07.2022_Working_with_page_model
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
        print('user', user)
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
<<<<<<< HEAD
=======


class UpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = (UpdateUserSerializer,)

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            raise ValidationError('Something go wrong')
        return Response(serializer.data, status=status.HTTP_200_OK)
>>>>>>> _26.07.2022_Working_with_page_model
