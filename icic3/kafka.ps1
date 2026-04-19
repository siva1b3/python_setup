docker exec svcb3 kafka-topics --bootstrap-server localhost:9092 --create --topic text-events --partitions 1 --replication-factor 1

docker exec svcb3 kafka-topics --bootstrap-server localhost:9092 --create --topic image-events --partitions 1 --replication-factor 1

docker exec svcb3 kafka-topics --bootstrap-server localhost:9092 --list
