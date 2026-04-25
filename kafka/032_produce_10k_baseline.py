import time
from confluent_kafka import Producer

# Counters updated by callback. No printing per message.
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
    # poll(0) lets queued callbacks fire without blocking.
    # Without this, the internal queue can fill up on very large N.
    producer.poll(0)

producer.flush()

elapsed = time.perf_counter() - start

print(f"messages: {N}")
print(f"delivered: {delivered}")
print(f"failed: {failed}")
print(f"elapsed: {elapsed:.3f} s")
print(f"throughput: {N / elapsed:,.0f} msg/s")
