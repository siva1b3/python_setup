from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"FAILED: {err}")
        return
    print(
        f"OK: topic={msg.topic()} "
        f"partition={msg.partition()} "
        f"offset={msg.offset()} "
        f"key={msg.key().decode() if msg.key() else None}"
    )

producer = Producer({
    "bootstrap.servers": "kafka:29092",  "acks": "1"
})

for i in range(3):
    producer.produce(
        topic="demo",
        key=f"user-{i}",
        value=f"acks=0 message {i}",
        on_delivery=delivery_report,
    )

producer.flush()
print("done")