from core.Broker import Broker

from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError


class GooglePubSub(Broker):

    # TODO: set project_id globally

    def __init__(self):
        self.PROJECT_ID = "meow"
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()


    def create_topic(self, topic_id):
        topic_path = self.publisher.topic_path(self.PROJECT_ID, topic_id)
        topic = self.publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {topic.name}")

    
    def create_topics(self, topic_ids: list):
        for topic_id in topic_ids:
            self.create_topic(topic_id)


    def delete_topic(self, topic_id):
        topic_path = self.publisher.topic_path(self.PROJECT_ID, topic_id)
        self.publisher.delete_topic(request={"topic": topic_path})
        print(f"Deleted topic: {topic_path}")


    def delete_topics(self, topic_ids: list):
        for topic_id in topic_ids:
            self.delete_topic(topic_id)


    def list_topics(self):
        project_path = f"projects/{self.PROJECT_ID}"
        for topic in self.publisher.list_topics(request={"project": project_path}):
            print(topic)


    def create_publisher(self):
        return pubsub_v1.PublisherClient()


    def create_subscriber(self):
        return pubsub_v1.SubscriberClient()


    def publish(self, topic_id, data):
        topic_path = self.publisher.topic_path(self.PROJECT_ID, topic_id)
        data = data.encode("utf-8")
        future = self.publisher.publish(topic_path, data)
        print(f'Published Data: {future.result()}')


    def create_subscription(self, subscribe_topic_id):
        topic_path = self.publisher.topic_path(self.PROJECT_ID, subscribe_topic_id)
        subscription_path = self.subscriber.subscription_path(self.PROJECT_ID, subscribe_topic_id + '-id')

        subscription = self.subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

        print(f"Subscription created: {subscription}")


    def subscribe(self, subscribe_topic_id: str, timeout: float = None):
        # def callback(message: pubsub_v1.subscriber.message.Message):
        #     print(f"Subscribed Message: {message}.")
        #     message.ack()


        print(f'Subscribing {subscribe_topic_id}')

        # self.create_subscription(subscribe_topic_id)

        subscription_path = self.subscriber.subscription_path(self.PROJECT_ID, subscribe_topic_id + '-id')
        print('Subscription path done')

        response = self.subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 1,
            }
        )

        for msg in response.received_messages:
            print("Received message:", msg.message.data[:50])

        ack_ids = [msg.ack_id for msg in response.received_messages]
        if len(ack_ids) != 0:
            self.subscriber.acknowledge(
                request={
                    "subscription": subscription_path,
                    "ack_ids": ack_ids,
                }
            )

            return response.received_messages[0].message.data

        return None

        # streaming_pull_future = self.subscriber.subscribe(subscription_path, callback=callback)
        # print('Streaming pull created')

        # # # with self.subscriber:
        # try:
        #     r = streaming_pull_future.result(timeout=5.0) # TODO: REMOVE TIMEOUT
        #     print('Completed')
        #     print(r)
        # except TimeoutError:
        #     print('Timeout')
        #     streaming_pull_future.cancel()  # Trigger the shutdown.
        #     streaming_pull_future.result()  # Block until the shutdown is complete.

        # print('God Complete!')