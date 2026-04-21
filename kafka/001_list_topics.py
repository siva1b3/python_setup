from confluent_kafka.admin import AdminClient

# From inside the python-dev container (same Docker network as broker):
#   use the internal listener "kafka:29092"
# From your host machine (outside Docker):
#   use the external listener "localhost:9092"
BOOTSTRAP = "kafka:29092"

admin = AdminClient({"bootstrap.servers": BOOTSTRAP})

metadata = admin.list_topics(timeout=5)

print(f"Cluster ID: {metadata.cluster_id}")
print(f"Controller broker ID: {metadata.controller_id}")
print(f"Brokers ({len(metadata.brokers)}):")
for broker_id, broker in metadata.brokers.items():
    print(f"  id={broker_id}  host={broker.host}:{broker.port}")

print(f"Topics ({len(metadata.topics)}):")
for name, topic in metadata.topics.items():
    print(f"  {name}  partitions={len(topic.partitions)}")