# FlightDeck — Operations Event Monitoring Platform

## Project Overview

**What:** A backend platform that ingests high-volume operational events from multiple systems, stores them in purpose-built databases, enables search, real-time monitoring, and batch analytics.

**Why:** Learn the full backend engineering stack — Django, Kafka, Cassandra, Elasticsearch, HDFS, PySpark — by building one project that grows incrementally. Each step solves a problem the previous step could not handle.

**Domain:** Aerospace operations monitoring. Five source systems generate events (propulsion, navigation, communications, thermal, power). The platform ingests, stores, queries, searches, and analyzes these events.

---

## How to Use This Document

This document is **the single source of truth** for the FlightDeck project. It is designed to be:

- **Portable** — paste into any Claude chat to resume work from where you left off
- **Idempotent** — contains full context, no dependency on chat history
- **Trackable** — update the progress tracker below as you complete steps

### Resuming in a New Chat

Paste this document and say:

> "I'm working on the FlightDeck project. I've completed up to Step X. Here's my plan document. Let's continue with Step Y."

### Progress Tracker

| Step | Name | Status | Date Completed | Run On |
|------|------|--------|----------------|--------|
| 0 | Simulator | NOT STARTED | | Local |
| 1 | First API + Docker | NOT STARTED | | Local |
| 2 | Add PostgreSQL | NOT STARTED | | Local |
| 3 | Read endpoints | NOT STARTED | | Local |
| 4 | Stress test | NOT STARTED | | Local |
| 5 | Add Kafka + Dozzle | NOT STARTED | | Local |
| 6 | Kafka consumer | NOT STARTED | | Local |
| 7 | Consumer resilience + DLQ | NOT STARTED | | Local |
| 8 | Add Prometheus + Grafana | NOT STARTED | | Local |
| 9 | Push PostgreSQL to limits | NOT STARTED | | Local |
| 10 | Add Cassandra | NOT STARTED | | EC2 |
| 11 | Add Elasticsearch | NOT STARTED | | EC2 |
| 12 | Add Loki + Promtail | NOT STARTED | | EC2 |
| 13 | Add OpenTelemetry + Tempo | NOT STARTED | | EC2 |
| 14 | Add HDFS | NOT STARTED | | EC2 |
| 15 | Add PySpark | NOT STARTED | | EC2 |
| 16 | End-to-end verification | NOT STARTED | | EC2 |

**Local:** Steps 0-9 run on your PC (7GB RAM sufficient)
**EC2:** Steps 10-16 run on AWS EC2 t3.xlarge (16GB RAM). Push code to Git, clone on EC2, continue.

---

## Development Philosophy

### No Local Python

Python is not installed on the host machine. All development happens inside a Python Docker container. VS Code Remote Containers attaches to the running dev container.

### Split Compose Architecture

During development, each concern is isolated in its own compose file. Start, stop, and rebuild any layer without touching the others. After development, one single prod compose file runs the entire system.

| File | Owns | When to restart |
|---|---|---|
| `dev/docker-compose.network.yml` | Creates `flightdeck-network` bridge network | Almost never — only if network is deleted |
| `dev/docker-compose.infra.yml` | Observability tools — Dozzle, Prometheus, Grafana, Loki, Tempo, OTel | When adding a new observability tool |
| `dev/docker-compose.app.yml` | Application services — Python dev container, PostgreSQL, Kafka, Cassandra, ES, HDFS, Spark | When adding a new data service |
| `dev/docker-compose.k6.yml` | k6 load runner — profile-gated, runs and exits | When running load tests |

All four files attach to the same external network `flightdeck-network`. Containers resolve each other by service name across files.

### Dev Container Pattern

One Python dev container holds all application code. During development, you run services manually inside it:

```
# Terminal 1 — Django API
cd /workspace/api && python manage.py runserver 0.0.0.0:8000

# Terminal 2 — Kafka consumer
cd /workspace/consumer && python consumer.py

# Terminal 3 — Search consumer
cd /workspace/search-consumer && python search_consumer.py
```

VS Code attaches to this container. You write code, run it, debug it — all inside the container.

### Dev vs Prod

| | Dev | Prod |
|---|---|---|
| Code source | Mounted from host via volume | `COPY` baked into image |
| Dependencies | `pip install` manually in container | `RUN pip install` in Dockerfile |
| Services | All run manually in one container | Each service in its own container |
| Observability | Dozzle + tools added per step | No Dozzle, full observability stack |
| k6 | On-demand via profile | Not included |
| Start command | Multiple compose files in order | `docker compose -f docker-compose.prod.yml up -d --build` |

### Idempotency Guarantee

Every compose file is idempotent. Running `docker compose up -d` twice produces the same result as running it once. If a container is already running and config hasn't changed, Docker skips it.

### Startup Order (Development)

```bash
# Step 1 — network first, always
docker compose -f dev/docker-compose.network.yml up -d

# Step 2 — infrastructure (observability)
docker compose -f dev/docker-compose.infra.yml up -d

# Step 3 — application services
docker compose -f dev/docker-compose.app.yml up -d

# Step 4 — attach VS Code to dev container
# VS Code → Remote Explorer → Dev Containers → flightdeck-dev → Attach

# Step 5 — k6 (on demand only)
docker compose -f dev/docker-compose.k6.yml --profile load run --rm k6 run /scripts/stress_test.js
```

### Shutdown Order (always reverse)

```bash
docker compose -f dev/docker-compose.app.yml down
docker compose -f dev/docker-compose.infra.yml down
docker compose -f dev/docker-compose.network.yml down
```

### Production (single command)

```bash
# Start everything
docker compose -f docker-compose.prod.yml up -d --build

# Stop everything
docker compose -f docker-compose.prod.yml down
```

---

## Directory Structure

Grows with each step. Only add files/folders when the step requires them.

```
flightdeck/
├── FLIGHTDECK_PLAN.md                          # This file
├── .gitignore
├── README.md
│
├── dev/                                         # Development compose files
│   ├── docker-compose.network.yml               # Step 1 — shared network
│   ├── docker-compose.infra.yml                 # Step 5+ — observability (grows)
│   ├── docker-compose.app.yml                   # Step 1+ — app services (grows)
│   └── docker-compose.k6.yml                    # Step 4 — load testing
│
├── docker-compose.prod.yml                      # Step 1+ — full system (grows)
│
├── src/                                         # All application code
│   ├── simulator/
│   │   ├── simulator.py                         # Step 0
│   │   ├── requirements.txt                     # Step 0
│   │   └── events.json                          # Step 4 — pre-generated for k6
│   │
│   ├── api/                                     # Django REST API
│   │   ├── Dockerfile                           # Step 1 (for prod)
│   │   ├── requirements.txt                     # Step 1
│   │   ├── manage.py                            # Step 1
│   │   └── flightdeck/                          # Django project
│   │       ├── __init__.py
│   │       ├── settings.py
│   │       ├── urls.py
│   │       ├── wsgi.py
│   │       └── events/                          # Django app
│   │           ├── __init__.py
│   │           ├── models.py                    # Step 2
│   │           ├── serializers.py               # Step 2
│   │           ├── views.py                     # Step 1
│   │           ├── urls.py                      # Step 1
│   │           ├── metrics.py                   # Step 8
│   │           ├── kafka_producer.py            # Step 5
│   │           └── management/
│   │               └── commands/
│   │                   └── seed.py              # Step 2
│   │
│   ├── consumer/                                # Step 6 — Kafka → PostgreSQL/Cassandra
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── consumer.py
│   │   ├── metrics.py                           # Step 8
│   │   └── config.py
│   │
│   ├── search-consumer/                         # Step 11 — Kafka → Elasticsearch
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── search_consumer.py
│   │
│   ├── archive-consumer/                        # Step 14 — Kafka → HDFS
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── archive_consumer.py
│   │
│   └── spark-jobs/                              # Step 15 — PySpark batch
│       ├── aggregate_events.py
│       └── submit.sh
│
├── k6/                                          # Step 4
│   └── stress_test.js
│
├── config/                                      # Service configurations
│   ├── prometheus/                              # Step 8
│   │   └── prometheus.yml
│   ├── grafana/                                 # Step 8
│   │   └── provisioning/
│   │       ├── datasources/
│   │       │   ├── prometheus.yml               # Step 8
│   │       │   ├── loki.yml                     # Step 12
│   │       │   └── tempo.yml                    # Step 13
│   │       └── dashboards/
│   ├── promtail/                                # Step 12
│   │   └── config.yml
│   ├── tempo/                                   # Step 13
│   │   └── tempo.yml
│   ├── otel-collector/                          # Step 13
│   │   └── otel-collector.yml
│   └── cassandra/                               # Step 10
│       └── init.cql
│
└── docs/                                        # Optional notes per step
    └── step-XX-notes.md
```

---

## Event Schema

Used across all steps. Every component produces and consumes this format.

```json
{
  "source_system": "propulsion-monitor",
  "event_type": "ERROR",
  "message": "Hydraulic pressure exceeded threshold: 3200 PSI",
  "metadata": {
    "sensor_id": "HYD-042",
    "reading": 3200,
    "threshold": 3000,
    "unit_id": "aircraft-7"
  },
  "timestamp": "2026-03-21T14:32:07.123Z"
}
```

### Source Systems (5)

| System | INFO messages | WARN messages | ERROR messages |
|--------|-------------|---------------|----------------|
| propulsion-monitor | Engine start successful, Thrust nominal, Fuel flow stable | Vibration above normal, Fuel consumption high | Hydraulic pressure exceeded threshold, Engine overheat detected, Thrust vectoring failure |
| nav-system | GPS lock acquired, Waypoint reached, Altitude stable | GPS signal degraded, Heading drift detected | GPS lock lost, INS alignment failure, Altitude deviation critical |
| comms-relay | Uplink established, Telemetry transmitted, Handoff complete | Signal strength low, Latency above threshold | Uplink lost, Telemetry gap detected, Frequency interference |
| thermal-control | Coolant flow nominal, Bay temperature stable | Temperature approaching limit, Coolant pressure low | Thermal runaway detected, Coolant system failure, Sensor malfunction |
| power-distribution | Bus voltage nominal, Battery charged, Load balanced | Voltage fluctuation detected, Battery below 30% | Bus fault detected, Generator offline, Load shedding activated |

### Metadata per System

| System | Fields |
|--------|--------|
| propulsion-monitor | sensor_id, reading, threshold, unit_id, engine_number |
| nav-system | latitude, longitude, altitude, heading, speed, satellite_count |
| comms-relay | frequency, signal_strength_dbm, link_id, bandwidth_kbps |
| thermal-control | sensor_id, temperature_c, zone, coolant_flow_rate |
| power-distribution | bus_id, voltage, current_amps, load_percentage |

### Event Type Distribution

- 70% INFO
- 20% WARN
- 10% ERROR

---

## Container Inventory

### Application Containers (dev/docker-compose.app.yml)

| # | Container | Image | Port | Added | Purpose |
|---|-----------|-------|------|-------|---------|
| 1 | flightdeck-dev | python:3.14-slim-bookworm | 8000-8004 | Step 1 | Dev container — all code here |
| 2 | flightdeck-db | postgres:18-bookworm | 5432 | Step 2 | PostgreSQL |
| 3 | flightdeck-kafka | confluentinc/cp-kafka:8.1.2 | 9092 | Step 5 | Kafka (KRaft) |
| 4 | flightdeck-cassandra | cassandra:5.0.7 | 9042 | Step 10 | Event storage |
| 5 | flightdeck-elasticsearch | elasticsearch:9.3.2 | 9200 | Step 11 | Full-text search |
| 6 | flightdeck-namenode | bde2020/hadoop-namenode | 9870 | Step 14 | HDFS metadata |
| 7 | flightdeck-datanode | bde2020/hadoop-datanode | 9864 | Step 14 | HDFS storage |
| 8 | flightdeck-spark-master | apache/spark:4.0.2 | 8080 | Step 15 | Spark master |
| 9 | flightdeck-spark-worker | apache/spark:4.0.2 | — | Step 15 | Spark executor |

### Observability Containers (dev/docker-compose.infra.yml)

| # | Container | Image | Port | Added | Purpose |
|---|-----------|-------|------|-------|---------|
| 10 | flightdeck-dozzle | amir20/dozzle:v10 | 9999 | Step 5 | Log viewer |
| 11 | flightdeck-prometheus | prom/prometheus:v3.7.3 | 9090 | Step 8 | Metrics |
| 12 | flightdeck-grafana | grafana/grafana:12.3 | 3000 | Step 8 | Dashboards |
| 13 | flightdeck-loki | grafana/loki:3.6.1 | 3100 | Step 12 | Log aggregation |
| 14 | flightdeck-promtail | grafana/promtail:3.6.10 | — | Step 12 | Log shipping |
| 15 | flightdeck-otel | otel/opentelemetry-collector-contrib:0.140.0 | 4317, 4318 | Step 13 | Telemetry |
| 16 | flightdeck-tempo | grafana/tempo:2.10.3 | 3200 | Step 13 | Traces |

### Production-Only Containers (docker-compose.prod.yml adds these)

| # | Container | Image | Port | Purpose |
|---|-----------|-------|------|---------|
| P1 | api | Custom Dockerfile | 8000 | Django API |
| P2 | consumer | Custom Dockerfile | 8001 | Kafka → Cassandra |
| P3 | search-consumer | Custom Dockerfile | 8002 | Kafka → ES |
| P4 | archive-consumer | Custom Dockerfile | 8004 | Kafka → HDFS |

**Dev:** Up to 16 containers (dev container + data services + observability)
**Prod:** Up to 19 containers (each service separate + data + observability minus Dozzle)

---

## Observability Progression

| Step | Tool | Compose File | Why Now |
|------|------|-------------|---------|
| 0 | Structured JSON logging | — | Free. Avoids refactoring later |
| 5 | Dozzle | infra | 4 containers — need to see logs |
| 8 | Prometheus + Grafana | infra | Need numbers: throughput, lag, latency |
| 12 | Loki + Promtail | infra | 7+ services — search/correlate logs |
| 13 | OpenTelemetry + Tempo | infra | Per-event tracing across pipeline |

---

## API Endpoints (cumulative)

### Step 1 — In-memory

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| POST | /api/events/ | 201 | In-memory list |

### Step 2 — PostgreSQL

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| POST | /api/events/ | 201 | PostgreSQL |

### Step 3 — Read endpoints

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| POST | /api/events/ | 201 | PostgreSQL |
| GET | /api/events/ | Paginated list | PostgreSQL |
| GET | /api/events/?source={name} | Filter by source | PostgreSQL |
| GET | /api/events/?type={type} | Filter by type | PostgreSQL |
| GET | /api/events/?from={date}&to={date} | Filter by date | PostgreSQL |
| GET | /api/events/{id}/ | Single event | PostgreSQL |
| GET | /api/sources/ | List sources | PostgreSQL |
| GET | /api/health/ | Health check | PostgreSQL |

### Step 5 — Kafka (POST changes)

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| POST | /api/events/ | **202** | **Kafka** |

### Step 10 — Cassandra (GET changes)

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| GET | /api/events/?source={name} | Filter | **Cassandra** |
| GET | /api/events/?type={type} | Filter | **Cassandra** |

### Step 11 — Elasticsearch (new)

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| GET | /api/search/?q={keyword} | Search | Elasticsearch |
| GET | /api/search/?q={keyword}&source={name} | Filtered search | Elasticsearch |
| GET | /api/search/?q={keyword}&type={type}&from={date}&to={date} | Full search | Elasticsearch |

### Step 15 — PySpark stats (new)

| Method | URL | Response | Backend |
|--------|-----|----------|---------|
| GET | /api/stats/hourly/{source}/ | Hourly stats | Cassandra |
| GET | /api/stats/hourly/{source}/?from={date}&to={date} | Filtered stats | Cassandra |

---

## Step-by-Step Detailed Breakdown

---

### Step 0 — Simulator

**Objective:** Create test data to develop against.

**What you learn:** Python scripting, JSON structure, command-line arguments, Faker library.

**New containers:** None. Run using `docker run --rm -it -v ./src:/workspace python:3.14-slim-bookworm bash` before Step 1 dev container exists, or wait for Step 1.

**Compose files changed:** None.

**Files created:**
```
src/simulator/
├── simulator.py
└── requirements.txt
```

**requirements.txt:**
```
requests
faker
```

**What simulator.py does:**
1. Picks random source system (equal weight across 5)
2. Picks event type: 70% INFO, 20% WARN, 10% ERROR
3. Generates message from templates (see Source Systems table)
4. Generates metadata specific to source system (see Metadata table)
5. Generates ISO 8601 timestamp

**Modes:**
```bash
python simulator.py --mode burst --count 100 --dry-run
python simulator.py --mode stream --rate 5 --dry-run
python simulator.py --mode burst --count 1000 --target http://localhost:8000/api/events/
python simulator.py --mode stream --rate 10 --target http://localhost:8000/api/events/
```

**Console output:**
```
[001] INFO  propulsion-monitor | Engine start successful | {"sensor_id": "ENG-012", ...}
[002] ERROR nav-system         | GPS lock lost           | {"latitude": 17.385, ...}
...
Summary: 100 events | INFO: 71 | WARN: 19 | ERROR: 10
```

**Done when:**
- Correct schema, varied messages, correct metadata per system
- Distribution ~70/20/10 over 1000 events
- Both modes work

**Problem:** Events go nowhere.

---

### Step 1 — First API + Docker

**Objective:** Accept events over HTTP.

**What you learn:** Django setup, Docker, Dockerfile, docker-compose, dev container, VS Code remote, structured JSON logging.

**New containers:** flightdeck-dev

**Containers running:** 1

**Compose files created:**
```
dev/docker-compose.network.yml
dev/docker-compose.app.yml
docker-compose.prod.yml
```

**dev/docker-compose.network.yml:**
```yaml
name: flightdeck-network-manager

networks:
  flightdeck-network:
    driver: bridge
    name: flightdeck-network

services:
  network-anchor:
    image: busybox
    container_name: flightdeck-network-anchor
    networks:
      - flightdeck-network
    command: tail -f /dev/null
    restart: unless-stopped
```

**dev/docker-compose.app.yml:**
```yaml
name: flightdeck-app

services:
  flightdeck-dev:
    image: python:3.14-slim-bookworm
    container_name: flightdeck-dev
    working_dir: /workspace
    ports:
      - "8000:8000"
      - "8001:8001"
      - "8002:8002"
      - "8004:8004"
    volumes:
      - ../src:/workspace
    networks:
      - flightdeck-network
    command: tail -f /dev/null
    restart: unless-stopped

networks:
  flightdeck-network:
    external: true
```

**Files created:**
```
src/api/
├── Dockerfile
├── requirements.txt
├── manage.py
└── flightdeck/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── events/
        ├── __init__.py
        ├── views.py
        └── urls.py
```

**API:** POST /api/events/ → validate → store in Python list → return 201.

**Logging:** python-json-logger, every log line is JSON with timestamp, level, logger, message.

**Dev workflow:**
```bash
docker compose -f dev/docker-compose.network.yml up -d
docker compose -f dev/docker-compose.app.yml up -d
# Attach VS Code to flightdeck-dev
# Inside container:
cd /workspace/api
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

**Done when:** Simulator sends 10 events → 201. Restart API → events gone.

**Problem:** Events lost on restart.

---

### Step 2 — Add PostgreSQL

**Objective:** Persist events.

**What you learn:** Docker Compose multi-service, PostgreSQL, Django models, ORM, migrations.

**New containers:** flightdeck-db

**Containers running:** 2

**Compose files changed:** dev/docker-compose.app.yml (add db), docker-compose.prod.yml (add db)

**Models:** SourceSystem (name, description, is_active), Event (UUID id, FK source_system, event_type, message, metadata JSON, timestamp, created_at). Indexes on (source_system, timestamp) and (event_type, timestamp).

**Seed:** `python manage.py seed` creates 5 source systems. Idempotent.

**Done when:** 100 events persist across API restart.

**Problem:** No way to read events back via API.

---

### Step 3 — Read Endpoints

**Objective:** Query stored events.

**What you learn:** DRF serializers, filtering, pagination.

**New containers:** None

**Endpoints:** GET /api/events/ with filters (source, type, from, to, limit, offset). GET /api/events/{id}/. GET /api/sources/. GET /api/health/.

**Done when:** All filters work, pagination works.

**Problem:** Works at low volume. What about real load?

---

### Step 4 — Stress Test

**Objective:** Find the breaking point.

**What you learn:** Load testing, k6, bottleneck identification.

**New containers:** None (k6 on demand)

**Compose files created:** dev/docker-compose.k6.yml

**Flow:**
1. Simulator burst 5000 events → observe slowness
2. Add timing middleware to Django
3. k6 ramps 50→200 req/sec, measure latency
4. `docker stats` during test

**Expected:** Latency spikes at high load. Root cause: synchronous DB writes.

**Done when:** k6 shows degradation. Can explain the bottleneck.

**Problem:** API blocks on DB writes.

---

### Step 5 — Add Kafka + Dozzle

**Objective:** Decouple API from DB writes.

**What you learn:** Kafka (broker, topic, partition, producer), KRaft, confluent-kafka, 202 vs 201, Dozzle.

**New containers:** flightdeck-kafka, flightdeck-dozzle

**Containers running:** 4

**Compose files changed:** dev/docker-compose.app.yml (add kafka), dev/docker-compose.infra.yml (created, add dozzle)

**Kafka:** Topic `flightdeck-events`, 3 partitions, key=source_system, 7 day retention.

**API change:** POST → validate → Kafka publish → 202 Accepted. No DB write.

**Re-run k6:** Compare with Step 4. Latency drops.

**Done when:** 202 responses, events in Kafka, DB empty, Dozzle shows logs.

**Problem:** Events in Kafka, nobody reads them.

---

### Step 6 — Kafka Consumer

**Objective:** Move events from Kafka to PostgreSQL.

**What you learn:** Kafka consumer (group, offset, partition), batch writes, microservice.

**New containers:** None in dev (runs in dev container). Consumer container in prod only.

**Containers running:** 4

**Files created:** src/consumer/ (consumer.py, config.py, Dockerfile, requirements.txt)

**Consumer:** Group `event-writers`, batch 500 or 5s, bulk INSERT, commit after write.

**Dev:** Run `python consumer.py` manually in Terminal 2 inside dev container.

**Done when:** 1000 events flow end-to-end: simulator → API → Kafka → consumer → PostgreSQL.

**Problem:** What if consumer crashes?

---

### Step 7 — Consumer Resilience + DLQ

**Objective:** Prove no data loss on failure.

**What you learn:** Offset management, at-least-once delivery, DLQ pattern.

**New containers:** None

**DLQ topic:** `flightdeck-events-dlq`

**Test 1:** Stop consumer → send events → restart → all processed, zero loss.
**Test 2:** Send malformed message → lands in DLQ → consumer continues.

**Done when:** Both tests pass.

**Problem:** Can't measure — events/sec? lag? latency?

---

### Step 8 — Add Prometheus + Grafana

**Objective:** Measure the system with numbers.

**What you learn:** Prometheus (counters, gauges, histograms), /metrics, Grafana dashboards, PromQL.

**New containers:** flightdeck-prometheus, flightdeck-grafana

**Containers running:** 6

**Compose files changed:** dev/docker-compose.infra.yml (add prometheus, grafana)

**Files created:** config/prometheus/prometheus.yml, config/grafana/provisioning/..., metrics.py in api and consumer.

**API metrics (8000/metrics):** http_requests_total, http_request_duration_seconds, events_published_total, kafka_publish_errors_total.

**Consumer metrics (8001/metrics):** events_consumed_total, events_batch_write_duration_seconds, consumer_lag, dlq_messages_total.

**Dashboard:** Request rate, latency p50/p95/p99, Kafka publish rate, consumer rate, consumer lag, DLQ count.

**Done when:** Grafana shows live data. Consumer lag visible when stopping/restarting.

**Problem:** PostgreSQL is the only event store.

---

### Step 9 — Push PostgreSQL to Its Limits

**Objective:** See where PostgreSQL breaks.

**What you learn:** DB limits, EXPLAIN ANALYZE, why general-purpose DB struggles with time-series.

**New containers:** None

**Flow:** Send 1M+ events. Watch Grafana. Test queries. EXPLAIN ANALYZE. Check table size.

**Done when:** Measurable degradation with 1M+ rows.

**Problem:** PostgreSQL not designed for this pattern.

---

### Step 10 — Add Cassandra

**Objective:** High-volume event storage with query-specific tables.

**What you learn:** Cassandra (partition key, clustering key), CQL, denormalization, cassandra-driver.

**NOTE: This step and all following run on EC2. Push code to Git, clone on EC2.**

**New containers:** flightdeck-cassandra

**Containers running:** 7

**Cassandra tables:** events_by_source (PK: source_system), events_by_type (PK: event_type). Both cluster by timestamp DESC.

**Consumer change:** Dual write to both tables. No more PostgreSQL events.

**API change:** GET reads from Cassandra.

**New metrics:** cassandra_write_duration_seconds, cassandra_write_errors_total.

**Done when:** 10k events in both tables. GET returns correct data. PostgreSQL has zero events.

**Problem:** Can't search "find events mentioning hydraulic pressure."

---

### Step 11 — Add Elasticsearch

**Objective:** Full-text search.

**What you learn:** ES index, mapping, text vs keyword, bool query, second consumer group.

**New containers:** flightdeck-elasticsearch (search-consumer runs in dev container)

**Containers running:** 8

**ES mapping:** event_id (keyword), source_system (keyword), event_type (keyword), message (text), metadata (object), timestamp (date).

**Search consumer:** Group `search-indexers`, bulk index 500/5s. Independent from event-writers.

**New endpoints:** GET /api/search/?q=... with optional source, type, from, to filters.

**Done when:** Search finds events by keyword. Both consumers independent.

**Problem:** 7+ containers, correlating logs is painful.

---

### Step 12 — Add Loki + Promtail

**Objective:** Search/correlate logs across all services.

**What you learn:** Loki, Promtail, LogQL, Grafana log panels.

**New containers:** flightdeck-loki, flightdeck-promtail

**Containers running:** 10

**Compose files changed:** dev/docker-compose.infra.yml (add loki, promtail)

**How:** Promtail auto-discovers Docker containers, ships JSON logs to Loki. Grafana queries Loki alongside Prometheus.

**Done when:** Can query logs across all containers in Grafana.

**Problem:** Can't trace one event across the pipeline.

---

### Step 13 — Add OpenTelemetry + Tempo

**Objective:** Trace single events through the pipeline.

**What you learn:** Distributed tracing (trace, span, trace_id), OpenTelemetry, Tempo.

**New containers:** flightdeck-otel, flightdeck-tempo

**Containers running:** 12

**Trace flow:**
```
API: receive → kafka-publish
  ├── Consumer: consume → cassandra-write
  └── SearchConsumer: consume → es-index
```

**Done when:** Traces visible in Grafana/Tempo.

**Problem:** No batch analytics on historical data.

---

### Step 14 — Add HDFS

**Objective:** Long-term event archive.

**What you learn:** HDFS (namenode, datanode), WebHDFS, third consumer group.

**WARNING: HDFS Docker is fragile. Budget extra time.**

**New containers:** flightdeck-namenode, flightdeck-datanode (archive-consumer in dev container)

**Containers running:** 14

**Archive consumer:** Group `event-archivers`, flush 1000 events or 60s to HDFS as JSON files. Path: /data/events/YYYY/MM/DD/HH/

**Done when:** HDFS has JSON files. All three consumers independent.

**Problem:** Raw files, no aggregations.

---

### Step 15 — Add PySpark

**Objective:** Batch analytics.

**What you learn:** Spark (driver, executor, DataFrame), PySpark, HDFS→Cassandra.

**New containers:** flightdeck-spark-master, flightdeck-spark-worker

**Containers running:** 16

**Spark job:** Read HDFS → aggregate per source per hour → write Cassandra hourly_stats.

**New Cassandra table:** hourly_stats (PK: source_system, CK: hour_bucket DESC).

**New endpoint:** GET /api/stats/hourly/{source}/

**Done when:** Spark job produces correct stats. Endpoint returns them.

**Problem:** None — pipeline complete.

---

### Step 16 — End-to-End Verification

**Objective:** Prove everything works.

**All containers running.**

| # | Test |
|---|------|
| 1 | Stream 6000 events → verify counts in Cassandra, ES, HDFS |
| 2 | Search known keywords → correct results |
| 3 | Stop one consumer → others keep working |
| 4 | Kill consumer → restart → zero data loss |
| 5 | Spark job → verify hourly_stats |
| 6 | Grafana metrics + Loki logs + Tempo traces populated |
| 7 | Burst 10k → no crashes, lag returns to 0 |

**Done when:** All 7 tests pass.

---

## Technology Summary

| Technology | Role | Step |
|------------|------|------|
| Python | All application code | 0 |
| Django + DRF | REST API | 1 |
| Docker + Compose | Containers | 1 |
| PostgreSQL | Metadata, initial event store | 2 |
| k6 | Load testing | 4 |
| Kafka | Event streaming | 5 |
| Dozzle | Log viewer | 5 |
| Prometheus | Metrics | 8 |
| Grafana | Dashboards | 8 |
| Cassandra | Event storage | 10 |
| Elasticsearch | Search | 11 |
| Loki | Log aggregation | 12 |
| Promtail | Log shipping | 12 |
| OpenTelemetry | Tracing | 13 |
| Tempo | Trace storage | 13 |
| HDFS | Archive | 14 |
| PySpark | Batch analytics | 15 |

---

## Quick Reference — All Commands

```bash
# ── DEVELOPMENT ────────────────────────────────────────

# Start (in order)
docker compose -f dev/docker-compose.network.yml up -d
docker compose -f dev/docker-compose.infra.yml up -d
docker compose -f dev/docker-compose.app.yml up -d

# Attach VS Code to flightdeck-dev container

# Inside dev container — run services manually
cd /workspace/api && python manage.py runserver 0.0.0.0:8000
cd /workspace/consumer && python consumer.py
cd /workspace/search-consumer && python search_consumer.py
cd /workspace/archive-consumer && python archive_consumer.py

# Stop (reverse order)
docker compose -f dev/docker-compose.app.yml down
docker compose -f dev/docker-compose.infra.yml down
docker compose -f dev/docker-compose.network.yml down

# k6 (on demand)
docker compose -f dev/docker-compose.k6.yml --profile load run --rm k6 run /scripts/stress_test.js

# ── PRODUCTION ─────────────────────────────────────────

docker compose -f docker-compose.prod.yml up -d --build
docker compose -f docker-compose.prod.yml down

# ── KAFKA ──────────────────────────────────────────────

# List topics
docker exec flightdeck-kafka kafka-topics --list --bootstrap-server localhost:9092

# Read messages
docker exec flightdeck-kafka kafka-console-consumer \
  --topic flightdeck-events --from-beginning --bootstrap-server localhost:9092 --max-messages 5

# Check consumer lag
docker exec flightdeck-kafka kafka-consumer-groups \
  --bootstrap-server localhost:9092 --group event-writers --describe

# ── POSTGRESQL ─────────────────────────────────────────

docker exec flightdeck-db psql -U flightdeck -c "SELECT count(*) FROM events_event;"

# ── CASSANDRA ──────────────────────────────────────────

docker exec flightdeck-cassandra cqlsh -e "SELECT count(*) FROM flightdeck.events_by_source;"

# ── ELASTICSEARCH ──────────────────────────────────────

curl http://localhost:9200/flightdeck-events/_count

# ── HDFS ───────────────────────────────────────────────

docker exec flightdeck-namenode hdfs dfs -ls -R /data/events/

# ── GENERAL ────────────────────────────────────────────

docker stats                    # resource usage
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"   # container status
```

---

## Notes

- **Structured JSON logging** from Step 0. Non-negotiable.
- **Each consumer = independent Kafka consumer group.** Stopping one doesn't affect others.
- **PostgreSQL role shrinks:** Steps 1-9 stores events. Step 10+ only metadata.
- **HDFS Docker is fragile.** Extra time for Step 14.
- **Spark connector must match Spark version.** Pin at Step 15.
- **Redis not included.** Not in JD.
- **Steps 0-9 local (7GB RAM), Steps 10-16 EC2 (16GB RAM).**
