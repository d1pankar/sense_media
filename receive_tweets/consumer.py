from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, topic, server) -> None:
        self.topic = topic
        self.server = server
        self.consumer = KafkaConsumer(self.topic, bootstrap_servers=[self.server])

    def consume(self):
        print("Consumer listening...")
        for message in self.consumer:
            # print(json.loads(message.value.decode()))
            yield json.loads(message.value.decode())
