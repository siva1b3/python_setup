from confluent_kafka import Consumer

consumer = Consumer(
    {
        "bootstrap.servers": "kafka:29092",
        "group.id": "g2",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe(["demo"])

print("consumer g2 started, waiting for messages...")

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
