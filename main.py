from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
while True:
    data = json.dumps({"Hello": "there"}).encode("utf-8")
    print(data)
    producer.send("test-topic", value=data, key=data)
    print("Sent")
    time.sleep(1)
