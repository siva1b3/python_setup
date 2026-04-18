
docker exec etl-kafka kafka-topics --bootstrap-server localhost:9092  --create --topic text-events --partitions 1 --replication-factor 1

docker exec etl-kafka kafka-topics  --bootstrap-server localhost:9092  --create --topic image-events  --partitions 1  --replication-factor 1

docker exec etl-kafka kafka-topics  --bootstrap-server localhost:9092  --list