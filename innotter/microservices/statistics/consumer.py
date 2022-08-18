from confluent_kafka import Consumer

consumer = Consumer({'bootstrap.servers': 'localhost:29092', 'group.id': 'innotter',
                     'auto.offset.reset': 'earliest'})

consumer.subscribe(['user-stat'])
