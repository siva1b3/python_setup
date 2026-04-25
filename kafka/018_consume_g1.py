from confluent_kafka import Consumer

consumer = Consumer(
    {
        "bootstrap.servers": "kafka:29092",
        "group.id": "g1",
    }
)

consumer.subscribe(["demo"])

print("consumer started, waiting for messages...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"error: {msg.error()}")
            continue
        print(f"offset={msg.offset()} value={msg.value().decode('utf-8')}")
finally:
    consumer.close()
