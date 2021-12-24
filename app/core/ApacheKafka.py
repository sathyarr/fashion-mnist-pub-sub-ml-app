from core.Broker import Broker

from configparser import ConfigParser
from confluent_kafka import Producer
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka.admin import AdminClient, NewTopic


class ApacheKafka(Broker):


    def __init__(self, config_file_path):
        self.config_parser = ConfigParser()
        self.config_parser.read(config_file_path)

        self.default_config_dict = dict(self.config_parser['default'])

        self.default_consumer_config_dict = dict(self.config_parser['default'])
        self.default_consumer_config_dict.update(self.config_parser['consumer'])

        self.producer = Producer(self.default_config_dict)
        self.consumer = Consumer(self.default_consumer_config_dict)
        self.admin_client = AdminClient(self.default_config_dict)


    def create_topic(self, topic_id):
        self.create_topics([topic_id])


    def create_topics(self, topic_ids: list):
        topic_list = []
        for topic_id in topic_ids:
            topic_list.append(NewTopic(topic_id, 1, 1))
        self.admin_client.create_topics(topic_list)
        print(f"Created topics: {topic_ids}")


    def delete_topic(self, topic_id):
        self.delete_topics([topic_id])


    def delete_topics(self, topic_ids: list):
        self.admin_client.delete_topics(topic_ids)
        print(f"Deleted topics: {topic_ids}")

    def list_topics(self):
        print(self.admin_client.list_topics().topics)


    def create_publisher(self):
        return Producer(self.default_config_dict)


    def create_subscriber(self):
        return Consumer(self.default_consumer_config_dict)


    def publish(self, topic_id, data):
        def delivery_callback(err, msg):
            if err:
                print('ERROR: Message failed delivery: {}'.format(err))
            else:
                print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                    topic=msg.topic(), key=msg.key().decode('utf-8'), value=str(msg.value())[:50]))

        key = 'my_key'
        self.producer.produce(topic_id, data, key, callback=delivery_callback)
        self.producer.flush()

        print(f'Published Data: {key}')


    def subscribe(self, subscribe_topic_id):
        # Set up a callback to handle the '--reset' flag.
        # def reset_offset(consumer, partitions):
        #     if True: # TODO: Change to condition
        #         for p in partitions:
        #             p.offset = OFFSET_BEGINNING
        #         consumer.assign(partitions)

        print(f'Subscribing {subscribe_topic_id}')
        # consumer = Consumer(self.default_consumer_config_dict)
        self.consumer.subscribe([subscribe_topic_id]) #, on_assign=reset_offset)

        msg = self.consumer.poll(3.0)
        if msg is None:
            print("Waiting...")
        elif msg.error():
            print("ERROR: {}".format(msg.error()))
        else:
            print("Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=str(msg.value())[:10]))
            return msg.value()