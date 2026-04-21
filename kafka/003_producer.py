from confluent_kafka import Producer

BOOTSTRAP = "kafka:29092"

producer = Producer({"bootstrap.servers": BOOTSTRAP})

for i in range(10):
    producer.produce(topic="demo", value=f"msg-{i}")

# One flush after the loop, not inside it.
# Flushing per-message defeats batching and makes the producer synchronous.
producer.flush()

print("done — 10 messages queued and flushed")