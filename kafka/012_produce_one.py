from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "kafka:29092"})

producer.produce(topic="demo", value="hello")
producer.flush()

print("sent")