import abc

class Broker(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_topic():
        raise NotImplementedError


    @abc.abstractmethod
    def create_topics(topic_ids: list):
        raise NotImplementedError

    
    @abc.abstractmethod
    def delete_topic(topic_id):
        raise NotImplementedError


    @abc.abstractmethod
    def delete_topics(topic_ids: list):
        raise NotImplementedError


    @abc.abstractmethod
    def list_topics():
        raise NotImplementedError

    
    @abc.abstractmethod
    def create_publisher():
        raise NotImplementedError


    @abc.abstractmethod
    def create_subscriber():
        raise NotImplementedError


    @abc.abstractmethod
    def publish(topic_id, data):
        raise NotImplementedError


    @abc.abstractmethod
    def subscribe(subscribe_topic_id):
        raise NotImplementedError


    def create_subscription(self, subscribe_topic_id): # For Google PubSub only
        pass