import time
import utils

brokers = utils.get_all_brokers()

for broker_name, broker in brokers.items():

    print(f'\nInitializing {broker_name}')

    broker.list_topics()

    # active_broker = utils.get_active_broker_name()
    # if active_broker == 'apache-kafka': # Google PubSub once restarted, all topics will be emptied. Hence deleting again will caused Exception
    #     broker.delete_topic(utils.input_topic_name)
    #     # delay for the topic to get created successfully before proceeding
    #     time.sleep(5)
    #     broker.list_topics()

    broker.create_topic(utils.input_topic_name)
    # delay for the topic to get created successfully before proceeding
    time.sleep(5)

    if broker_name == 'google-pubsub':
        broker.create_subscription(utils.input_topic_name)

    broker.list_topics()