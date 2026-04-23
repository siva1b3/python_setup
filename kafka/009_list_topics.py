from confluent_kafka.admin import AdminClient

admin = AdminClient({"bootstrap.servers": "kafka:29092"})
metadata = admin.list_topics(timeout=5)

print(f"Broker count: {len(metadata.brokers)}")
for b_id, b in metadata.brokers.items():
    print(f"  Broker {b_id}: {b.host}:{b.port}")

print(f"Topic count: {len(metadata.topics)}")
for name, t in metadata.topics.items():
    print(f"  Topic: {name}  partitions={len(t.partitions)}")