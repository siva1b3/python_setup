from confluent_kafka import Producer

producer = Producer({"bootstrap.servers": "kafka:29092"})

siva = {
    "nafa": "siva",
    "bab": "lala",
    "car": "dada",
    "dar": "fafa"
}

producer.produce(
    topic="demo",
    key="user-1",
    value=str(siva),
)

producer.flush()
print("sent")