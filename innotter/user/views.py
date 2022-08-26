import json
import requests

from confluent_kafka import Producer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK

from user.serializers import LoginSerializer, UserRegistration, UpdateUserSerializer
from user.renderers import UserJSONRenderer
from user.permissions import UserUpdatePermission
from user.models import User

from statistic_client import StatisticClient

producer = Producer({'bootstrap.servers': 'localhost:29092'})


class RegistrationAPIView(APIView):
    """
    Class that realize functionality for register new user
    """
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

    permission_classes = [AllowAny]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserAPIView(UpdateAPIView):
    permission_classes = (UserUpdatePermission,)
    serializer_class = UpdateUserSerializer

    def put(self, request, *args, **kwargs):
        user = request.data
        instance = User.objects.get(email=user['email'])
        self.check_object_permissions(request=request, obj=instance)
        serializer = self.serializer_class(data=user, instance=instance)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserStatistic(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        email = request.user.email
        stat_url = f'http://127.0.0.1:8000//get_user_stat/{email}'
        user_stat = requests.get(url=stat_url)
        return Response(data=user_stat, status=HTTP_200_OK)


stat_client = StatisticClient()


class UserStatRabbit(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        email = request.user.email
        response = json.loads(stat_client.call(email=email))
        return Response(data=response, status=HTTP_200_OK)
