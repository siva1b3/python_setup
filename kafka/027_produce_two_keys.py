from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "kafka:29092"})

# 5 messages with key=user-1
for i in range(5):
    producer.produce(
        topic="demo",
        key="user-1",
        value=f"user-1 message {i}",
    )

# 5 messages with key=user-2
for i in range(5):
    producer.produce(
        topic="demo",
        key="user-2",
        value=f"user-2 message {i}",
    )

producer.flush()
print("sent 10 messages: 5 with user-1, 5 with user-2")