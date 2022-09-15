from confluent_kafka import Producer

import socket
import time


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


def send_test_messages():
    p = build_producer()
    topic = 'test'
    counter = 1

    while True:
        message = str(counter)
        send_asynchronously(p, topic, message)
        counter += 1
        time.sleep(1)


if __name__ == '__main__':
    send_test_messages()
