from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import LoginSerializer, UserRegistration, \
    UpdateUserSerializer
from user.renderers import UserJSONRenderer
from user.permissions import UserUpdatePermission
from user.models import User
from confluent_kafka import Producer
import json
import pika
import uuid

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


class StatisticClient:
    def __init__(self):
        self.corr_id = None
        self.response = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))

        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue="statistic")
        self.callback_queue = result.method.queue
        self.channel.basic_consume(on_message_callback=self.on_response, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            print(body)
            self.response = body

    def call(self, user_email):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(exchange='',
                                   routing_key="statistic",
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                   ),
                                   body=user_email)
        print("responce before while ", self.response)
        while self.response is None:
            self.connection.process_data_events()
            print(self.response)
        return self.response


user_statistic = StatisticClient()


class UserStatistic(ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        responce= user_statistic.call(request.user.email)
        print(responce)
        return Response(responce)
