import time
from confluent_kafka import Producer

delivered = 0
failed = 0
first_delivery_time = None
last_delivery_time = None


def delivery_report(err, msg):
    global delivered, failed, first_delivery_time, last_delivery_time
    now = time.perf_counter()
    if first_delivery_time is None:
        first_delivery_time = now
    last_delivery_time = now
    if err is not None:
        failed += 1
    else:
        delivered += 1


producer = Producer(
    {
        "bootstrap.servers": "kafka:29092",
        "acks": "all",
        "linger.ms": 50,
        "batch.size": 1024,
    }
)

N = 10_000
TOPIC = "demo"

t_start = time.perf_counter()

for i in range(N):
    producer.produce(
        topic=TOPIC,
        key=f"user-{i % 10}",
        value=f"msg-{i}",
        on_delivery=delivery_report,
    )
    producer.poll(0)

t_after_loop = time.perf_counter()

remaining = producer.flush(timeout=60)

t_after_flush = time.perf_counter()

print(f"messages produced (queued):      {N}")
print(f"delivered (callback fired OK):   {delivered}")
print(f"failed:                          {failed}")
print(f"flush() returned remaining:      {remaining}")
print(f"loop time (produce calls):       {t_after_loop - t_start:.3f} s")
print(f"flush time (wait for acks):      {t_after_flush - t_after_loop:.3f} s")
print(f"total elapsed:                   {t_after_flush - t_start:.3f} s")
if first_delivery_time and last_delivery_time:
    print(f"first callback at:               {first_delivery_time - t_start:.3f} s")
    print(f"last callback at:                {last_delivery_time - t_start:.3f} s")
