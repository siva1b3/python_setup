import time
from confluent_kafka import Producer

delivered = 0
failed = 0


def delivery_report(err, msg):
    global delivered, failed
    if err is not None:
        failed += 1
    else:
        delivered += 1


producer = Producer(
    {
        "bootstrap.servers": "kafka:29092",
        "acks": "all",
        "linger.ms": 50,  # NEW: wait up to 50 ms to batch messages
    }
)

N = 10_000
TOPIC = "demo"

start = time.perf_counter()

for i in range(N):
    producer.produce(
        topic=TOPIC,
        key=f"user-{i % 10}",
        value=f"msg-{i}",
        on_delivery=delivery_report,
    )
    producer.poll(0)

producer.flush()

elapsed = time.perf_counter() - start

print(f"messages: {N}")
print(f"delivered: {delivered}")
print(f"failed: {failed}")
print(f"elapsed: {elapsed:.3f} s")
print(f"throughput: {N / elapsed:,.0f} msg/s")
