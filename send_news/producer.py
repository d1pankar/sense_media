from kafka import KafkaProducer
import time
import json


class Producer:
    def __init__(self, topic, server) -> None:
        self.topic = topic
        self.server = server
        self.producer = KafkaProducer(bootstrap_servers=[self.server])

    def send(self, data):
        self.producer.send(self.topic, json.dumps(data).encode("utf-8"))
        time.sleep(1)
