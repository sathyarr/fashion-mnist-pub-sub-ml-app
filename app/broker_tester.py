from core.GooglePubSub import GooglePubSub
from core.ApacheKafka import ApacheKafka

import utils

kafka_config_file_path = utils.get_kafka_config()
broker = ApacheKafka(kafka_config_file_path)
# broker = GooglePubSub()

# broker.create_topic('input-topic')
# broker.create_subscription('input-topic')  # For Google PubSub only
broker.list_topics()

# broker.create_topics(['apple', 'mango', 'orange'])
# broker.list_topics()

# broker.delete_topic('input-topic')
# broker.list_topics()

# broker.delete_topics(['apple', 'mango'])
# broker.list_topics()

# print(broker.create_publisher())
# print(broker.create_subscriber())