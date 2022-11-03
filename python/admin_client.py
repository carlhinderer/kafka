import os

from configparser import ConfigParser

from confluent_kafka.admin import AdminClient, NewTopic


CONFIG_FILEPATH = os.path.join(os.getcwd(), 'config.ini')
TOPIC_NAME = 'test'


def get_config():
    config_parser = ConfigParser()
    config_parser.read_file(CONFIG_FILEPATH)
    config = dict(config_parser['default'])
    config['client.id'] = socket.gethostname()


def build_admin_client():
    config = get_config()
    return AdminClient(config)


def create_new_topic(admin_client, topic_name, num_partitions):
    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=1)
    new_topics = list(new_topic)
    fs = admin_client.create_topics(new_topics)

    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))


if __name__ == '__main__':
    admin_client = build_admin_client()
    create_new_topic(admin_client, TOPIC_NAME, 5)
