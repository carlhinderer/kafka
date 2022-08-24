from confluent_kafka import Producer

import socket


def build_producer():
    config = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()
    }

    return Producer(config)


def send_synchronously(producer, topic, value):
    producer.produce(topic, value=value)
    producer.flush()


def acked(err, msg):
    if err is not None:
        print("Error. Message: %s, Error: %s" % (str(msg), str(err)))
    else:
        print("Success. Message: %s" % str(msg))


def send_asynchronously(producer, topic, value):
    producer.produce(topic, value=value, callback=acked)
    producer.poll(1)  # Get delivery notification events, which triggers callbacks


if __name__ == '__main__':
    p = build_producer()
    topic = 'test'
    message = 'Hello, World'

    # send_synchronously(p, topic, message)
    send_asynchronously(p, topic, message)
