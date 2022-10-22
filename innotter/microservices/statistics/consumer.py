from confluent_kafka import Consumer
from innotter.microservices.statistics.view import load_statistic
import json

consumer = Consumer({'bootstrap.servers': 'localhost:29092',
                     'group.id': 'innotter',
                     'auto.offset.reset': 'earliest'
                     })

consumer.subscribe(['user-stat'])


def main():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        data = msg.value().decode('utf-8')
        data_json = json.loads(data)
        load_statistic(data_json)
    consumer.close()
