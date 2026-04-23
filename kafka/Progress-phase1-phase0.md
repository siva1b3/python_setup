# Kafka Learning — Progress

## Completed

### Phase 0 (Steps 1–9) — Environment
Set up single-broker Kafka in KRaft mode via Docker Compose, added AKHQ UI, and confirmed Python connectivity to the broker using `AdminClient.list_topics`.

- `docker-compose.network.yaml` — external `streaming-network` bridge
- `docker-compose.kafka.yml` — `kafka` broker + `akhq` UI
- `docker-compose.producer01.yaml` — `python-dev` container on same network
- `install.sh` — installs `confluent-kafka`
- `009_list_topics.py` — lists brokers and topics via AdminClient

### Phase 1 (Steps 10–15) — Topic + producer basics
Created topic `demo` (partitions=1) via AKHQ. Wrote messages from Python and observed offset behavior.

- `012_produce_one.py` — sends one `"hello"` message; demonstrated `flush()` requirement and offset increment on repeated runs
- `015_produce_ten.py` — loop producing `msg-0` through `msg-9`; confirmed per-partition monotonic offsets and automatic batching

**Key observations:**
- Offsets are per-partition, monotonic, never reused.
- `flush()` mandatory before producer exit.
- Use `kafka:29092` from inside Docker network, `localhost:9092` from host.
- AKHQ Data tab display order is unreliable — verify ordering with `kafka-console-consumer --from-beginning`.

## Environment state

- Topic `demo` exists, partitions=1, contains ~84 messages.
- All containers running: `kafka`, `akhq`, `python-dev`, `streaming-gateway`.
