from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "kafka:29092"})

for i in range(10):
    producer.produce(topic="demo", value=f"msg-{i}")

producer.flush()

print("sent 10 messages")