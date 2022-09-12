import json
import pika
# import django
from sys import path
from os import environ

# path.append('E:\innotter\innotter\innotter\settings.py')
# environ.setdefault('DJANGO_SETTINGS_MODULE', 'user.settings')
# django.setup()
# path.append('E:\innotter\innotter\user\models')
# path.append('E:\innotter\innotter\user\serializers')

from models import User
from user.serializers import UpdateUserSerializer

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='innotter')

serializer_class = UpdateUserSerializer


def callback(ch, method, properties, body):
    message = json.loads(body)
    instance = User.objects.get(email=message['email'])
    serializer = serializer_class(data=message, instance=instance)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume('innotter', callback, auto_ack=True)
channel.start_consuming()
