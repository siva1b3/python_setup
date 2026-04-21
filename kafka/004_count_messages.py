from confluent_kafka import Consumer, TopicPartition
from confluent_kafka.admin import AdminClient

BOOTSTRAP = "kafka:29092"
TOPIC = "demo"

admin = AdminClient({"bootstrap.servers": BOOTSTRAP})

# Consumer is used only for its get_watermark_offsets() method.
# group.id is required but no subscription is made, so no group is actually joined.
consumer = Consumer({
    "bootstrap.servers": BOOTSTRAP,
    "group.id": "watermark-probe",  # not used for commits
})

metadata = admin.list_topics(timeout=5)

if TOPIC not in metadata.topics:
    print(f"Topic '{TOPIC}' not found")
    consumer.close()
    raise SystemExit(1)

topic_meta = metadata.topics[TOPIC]

total = 0
print(f"Topic: {TOPIC}")
print(f"{'Partition':<12}{'Low':<10}{'High':<10}{'Count':<10}")

for partition_id in topic_meta.partitions:
    tp = TopicPartition(TOPIC, partition_id)
    low, high = consumer.get_watermark_offsets(tp, timeout=5)
    count = high - low
    total += count
    print(f"{partition_id:<12}{low:<10}{high:<10}{count:<10}")

print(f"Total messages across all partitions: {total}")

consumer.close()