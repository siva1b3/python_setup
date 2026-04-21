from confluent_kafka import Producer

# Same logic as the admin script:
# inside python-dev container -> use kafka:29092
# from host machine           -> use localhost:9092
BOOTSTRAP = "kafka:29092"

producer = Producer({"bootstrap.servers": BOOTSTRAP})

producer.produce(topic="demo", value="hello")

# flush() blocks until all queued messages are delivered (or fail).
# Without flush(), the script may exit before the message is sent.
producer.flush()

print("done")