import os
import socket
import time

from configparser import ConfigParser

from confluent_kafka import Producer


CONFIG_FILEPATH = 'config.ini'
TOPIC = 'test'


def get_config():
    config_parser = ConfigParser()
    config_parser.read(CONFIG_FILEPATH)
    config = dict(config_parser['default'])
    config['client.id'] = socket.gethostname()
    return config


def build_producer():
    config = get_config()
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
    counter = 1

    while True:
        message = str(counter)
        send_asynchronously(p, TOPIC, message)
        counter += 1
        time.sleep(1)


if __name__ == '__main__':    
    send_test_messages()
