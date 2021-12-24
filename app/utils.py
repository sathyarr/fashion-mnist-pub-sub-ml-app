import os
from core.GooglePubSub import GooglePubSub
from core.ApacheKafka import ApacheKafka

input_topic_name = 'input-topic'

def get_kafka_config():
    return os.environ['ML_APP_KAFKA_CONFIG']


brokers = {
    'apache-kafka': ApacheKafka(config_file_path=get_kafka_config()),
    'google-pubsub': GooglePubSub()
}


def get_all_brokers():
    return brokers


def get_broker():
    # os.environ[] won't change dynamically in runtime for Python. Hence, it always returns the value of program start
    ml_app_broker = os.environ['ML_APP_BROKER']
    return brokers[ml_app_broker]


def get_active_broker_name():
    return os.environ['ML_APP_BROKER']


def isfile_check_and_exit(input, msg):
    if not os.path.isfile(input):
        exit(msg)


def isdir_check_and_exit(input, msg):
    if not os.path.isdir(input):
        exit(msg)