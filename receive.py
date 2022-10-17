from kafka import KafkaConsumer
import json

while True:
    consumer = KafkaConsumer("test-topic", bootstrap_servers=["localhost:9092"])
    print(consumer.topics())

    for message in consumer:
        print(message)
        print(json.loads(message.value.decode()))

        print("REceived")
