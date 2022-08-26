import pika
import json
from generate_statistics import GetStatistics

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='statistic')

statistics_class = GetStatistics()


def get_statistic(email):
    user_stat = json.dumps(statistics_class.generate_statistic(email))
    return user_stat


def on_request(ch, method, props, body):
    email = body.decode("utf-8")
    print('got {}'.format(email))
    response = get_statistic(email)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id), body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='statistic', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
