# Kafka Learning — Cross-Chat Context

> Paste this entire file at the start of any new Claude chat to resume the roadmap from any step.

---

## How to use this file

1. Paste this whole file into a new Claude chat.
2. At the end, write: **"I am at Phase X, Step N. Help me with this step."**
3. Claude will assume all prior steps are complete and the exit state of the previous step is the current state.
4. Do not re-explain the roadmap. Claude reads it from this file.

---

## Context

I am learning Apache Kafka from zero. I already know Python and Node.js. My target is a **single-broker** Kafka setup only — multi-broker is out of scope.

**Stack:**
- Docker Compose, single Kafka broker in KRaft mode (no ZooKeeper).
- AKHQ as UI.
- Python client: `confluent-kafka-python` (wraps `librdkafka`). Not `kafka-python`.

**My background relevant to this learning:**
- Full-stack Python/Node.js developer.
- Comfortable with Docker, Postgres, FastAPI, system design.
- New to Kafka specifically.

---

## Rules for Claude

These rules apply to every response in this learning track:

1. **One small change per step.** No step introduces two new ideas at once. If a step seems to, split it.
2. **Observe before adding.** Every new config or concept must be observed in action before the next one is introduced.
3. **Build on previous step only.** Each step starts from the exit state of the previous step. Never assume a config or concept that was not introduced in an earlier step.
4. **No leaps.** If the gap between two steps feels large, insert intermediate steps.
5. **Single-broker scope only.** Do not introduce replication, ISR, multi-broker, MirrorMaker, or anything that requires more than one broker. Mark such things as "deferred" if they come up.
6. **Python only** for producer/consumer code. Do not give Java or Node.js examples unless I ask.
7. **Concrete over abstract.** Show real commands, real configs, real expected output. No vague advice.
8. **Challenge flawed assumptions.** If I state something incorrect, correct it directly with reasoning.
9. **Format:** Core answer first, then reasoning, tradeoffs, alternatives, edge cases as needed. No filler, no praise, no motivational language.
10. **English is my second language.** Use clear, precise wording. Avoid idioms.

---

## Roadmap (single-broker, Python)

Conventions: `P/C/T` = producers / consumers / topics. Partition count noted separately. Each step changes exactly one thing from the previous step.

---

### Phase 0 — Environment

**Goal:** Broker is running and reachable from Python.

1. Install Docker and Docker Compose. Verify `docker version`.
2. Create `docker-compose.yml` with one Kafka broker in KRaft mode, port `9092` exposed.
3. `docker compose up -d`. Verify with `docker ps`.
4. Check broker logs with `docker logs <kafka-container>` — confirm "Kafka Server started".
5. Add a named volume for broker data; restart compose; verify data persists.
6. Add AKHQ as a second service in the same compose file.
7. Open AKHQ in a browser; confirm the broker appears.
8. Create a Python virtualenv. `pip install confluent-kafka`.
9. Write a script that calls `AdminClient.list_topics(timeout=5)` and prints the result.

**Exit state:** Broker + UI running, Python connectivity confirmed.

---

### Phase 1 — One topic, one message

**Goal:** Create a topic and write one message to it.

10. In AKHQ, create topic `demo` with partitions=1, replication=1.
11. Confirm topic appears in AKHQ. Note "0 messages, 1 partition".
12. Write Python producer: `bootstrap.servers="localhost:9092"`, `produce("demo", value="hello")`, `flush()`. Run.
13. In AKHQ → topic `demo` → "Data" tab. Confirm message at offset `0`, partition `0`.
14. Run producer again. Observe second message at offset `1`. Note offsets are monotonic per partition.
15. Modify producer to send 10 messages `msg-0` through `msg-9`. Observe offsets `2`–`11` in AKHQ.

**Exit state:** Topic created, messages visible in UI with offsets.

---

### Phase 2 — One consumer, plain read

**Goal:** Read messages. Introduce minimum consumer config, then build up by observation.

16. Identify minimum required consumer configs: `bootstrap.servers`, `group.id`. Client refuses to start without `group.id`.
17. Understand `group.id`: identifies a consumer group; Kafka tracks committed offsets per group; same `group.id` = shared work, different `group.id` = independent copies.
18. Write consumer: `bootstrap.servers`, `group.id="g1"`. Subscribe to `["demo"]`. Loop: `poll(1.0)`, print value.
19. Run consumer. Observe: prints **nothing**. Stop.
20. Reason: default `auto.offset.reset=latest` means new groups start at the end of the log.
21. Run producer once more. Watch consumer print exactly that one new message. Confirms `latest` behavior.
22. Stop consumer. Add `auto.offset.reset="earliest"`. Change to `group.id="g2"`. Run.
23. Observe: consumer prints **all** messages from offset 0. Confirms `earliest` behavior.
24. Stop. Restart with same `g2`. Observe: prints **nothing new** — `auto.offset.reset` only applies when no committed offset exists.
25. In AKHQ → Consumer Groups → `g2`. See committed offset and lag = 0.

**Exit state:** `group.id` and `auto.offset.reset` understood by observation.

---

### Phase 3 — Producer: keys, then acknowledgement

**Goal:** Add producer features one at a time.

26. Modify producer to pass `key="user-1"`. In AKHQ, observe key column populated.
27. Send 5 messages with key `user-1`, 5 with key `user-2`. All still go to partition 0 (only one partition). Keys not yet meaningful.
28. Add delivery callback: `on_delivery=lambda err, msg: print(err, msg.offset())`. Observe callback fires after `flush()`.
29. Add `acks=1`. Behavior unchanged but contract explicit.
30. Change `acks=0`. Callback still reports success but broker did not confirm. Hard to demo failure on single broker — note for awareness.
31. Change `acks=all`. On single broker equivalent to `acks=1`. Production-correct default.

**Exit state:** Keys, delivery callbacks, and `acks` modes observed.

---

### Phase 4 — Producer: batching, then compression

**Goal:** Make producer efficient — one knob at a time.

32. Modify producer to send 10,000 messages tight loop, then `flush()`. Time it.
33. Add `linger.ms=50`. Re-time. Observe AKHQ throughput.
34. Add `batch.size=32768`. Re-run. Bigger batches when bursty.
35. Add `compression.type="lz4"`. Compare on-disk size: `docker exec` into broker, `du -sh /var/lib/kafka/data/demo-0/` before vs after.

**Exit state:** Batching and compression measured.

---

### Phase 5 — Producer: idempotence, then transactions

**Goal:** Strengthen producer guarantees, one level at a time.

36. Add `enable.idempotence=true`. Producer now has a Producer ID (PID). Prevents duplicates on internal retries within one session.
37. Idempotence requires `acks=all`, `max.in.flight.requests.per.connection ≤ 5`, `retries > 0`. Make explicit.
38. Add `transactional.id="p1"`. Call `producer.init_transactions()` once at startup.
39. Wrap produce in `begin_transaction()` / `commit_transaction()`. Run. Message arrives normally.
40. Replace commit with `abort_transaction()`. In AKHQ, message **does** appear but marked as part of aborted transaction.
41. On consumer add `isolation.level="read_committed"`. Re-run. Aborted message **not** seen. Switch back to `read_uncommitted` to confirm difference.

**Exit state:** Idempotence and transactions used; consumer isolation level observed.

---

### Phase 6 — Consumer: offset commits

**Goal:** Take control of commits.

42. Default behavior: `enable.auto.commit=true`, `auto.commit.interval.ms=5000`. Background commits.
43. Stop consumer mid-stream (Ctrl+C). Restart. Observe possible **replay** of last few messages.
44. Add `enable.auto.commit=false`. Process but never commit. Stop, restart. Observe full replay since last commit.
45. After each message, call `consumer.commit(message=msg, asynchronous=False)`. Stop mid-stream, restart. Resumes exactly.
46. Switch to `asynchronous=True`. Slightly faster; errors via callback.
47. Implement explicit **commit-after-process** pattern: `for msg: process(msg); commit(msg)`. This is at-least-once.

**Exit state:** Commit timing controlled.

---

### Phase 7 — Consumer: liveness and shutdown

**Goal:** Understand how broker decides consumer is alive or dead.

48. Defaults: `session.timeout.ms=45000`, `heartbeat.interval.ms=3000`, `max.poll.interval.ms=300000`. Print at startup.
49. Add `time.sleep(60)` after one message. Heartbeats run on separate thread — consumer stays in group.
50. Set `max.poll.interval.ms=10000`, `time.sleep(15)`. Broker kicks consumer; rebalance log line appears on next poll.
51. Implement graceful shutdown: trap SIGTERM/SIGINT, finish current message, commit, `consumer.close()`. Verify clean leave in AKHQ.

**Exit state:** Heartbeat vs poll-interval understood as separate liveness signals.

---

### Phase 8 — Consumer: positioning

**Goal:** Move consumer to arbitrary points in the log.

52. `consumer.seek(TopicPartition("demo", 0, 0))` after assignment to replay from offset 0 in one run.
53. `consumer.offsets_for_times([TopicPartition("demo", 0, <epoch_ms>)])` → seek to timestamp.
54. From inside broker container: `kafka-consumer-groups.sh --reset-offsets --to-earliest --group g1 --topic demo --execute`. Next run replays.

**Exit state:** Consumer positionable anywhere in log.

---

### Phase 9 — Delivery semantics

**Goal:** Implement each guarantee deliberately.

55. **At-most-once:** commit before processing. Inject crash after commit. Observe loss.
56. **At-least-once:** commit after processing. Inject crash between process and commit. Observe duplicate.
57. **Effective exactly-once on consumer side:** in-memory `set()` (or SQLite) of `(partition, offset)` already processed. Skip on replay.
58. **Kafka exactly-once:** consume-transform-produce loop. Consumer reads from `demo`, producer writes to `demo-out` inside transaction, `producer.send_offsets_to_transaction(offsets, consumer.consumer_group_metadata())`. Verify with `read_committed`.

**Exit state:** All four delivery semantics implemented.

---

### Phase 10 — Storage: segments and retention

**Goal:** See on-disk storage and deletion.

59. `docker exec` into broker. `/var/lib/kafka/data/demo-0/`. List `.log`, `.index`, `.timeindex`.
60. `kafka-dump-log.sh --files 00000000000000000000.log --print-data-log`. See raw records.
61. Topic config `segment.bytes=1048576`. Produce ~2 MB. New segment file appears.
62. `retention.ms=60000`. Wait > 1 min. Old closed segments deleted. Active segment never deleted by retention.
63. `retention.bytes=5242880`. Overflow. Size-based deletion.

**Exit state:** Segments and retention concrete.

---

### Phase 11 — Storage: log compaction

**Goal:** Observe `cleanup.policy=compact`.

64. Create `demo-compact`, partitions=1, `cleanup.policy=compact`, `min.cleanable.dirty.ratio=0.01`, `segment.ms=10000`.
65. Produce: `(k1, v1), (k2, v1), (k1, v2), (k1, v3), (k2, v2)`.
66. Wait. `kafka-dump-log.sh` to inspect. Eventually only `(k1, v3)` and `(k2, v2)` remain.
67. Send tombstone: key `k1`, value `None`. After compaction, `k1` gone entirely.

**Exit state:** Compaction observed.

---

### Phase 12 — Partitions

**Trigger:** with one partition, all messages serialized. Need parallelism or key-based routing.

**Goal:** Add partitions, observe behavior.

68. Create `demo-p3` with partitions=3.
69. Produce 30 messages with no key. Per-partition counts in AKHQ. Sticky partitioner — batches go to same partition for a while then rotate.
70. Produce 30 messages with `key=f"user-{i % 5}"`. Same key → same partition consistently.
71. Verify per-partition ordering: produce interleaved keyed messages (`u1, u2, u1, u2, u1`). `u1` ordered among themselves, `u2` ordered among themselves; no global order across partitions.
72. `kafka-topics.sh --alter --topic demo-p3 --partitions 5` succeeds. `--partitions 2` fails — partitions only increase.

**Exit state:** Partitioning and key routing concrete.

---

### Phase 13 — Consumer group parallelism

**Trigger:** one consumer reads all 3 partitions sequentially. Scale out the group.

**Goal:** Add consumers to one group.

73. Start consumer with `group.id=g3` on `demo-p3`. Assigned all 3 partitions.
74. Start second consumer same `group.id=g3`. Partitions split (e.g., 2+1).
75. Start third consumer. Even split (1+1+1).
76. Start fourth consumer. One **idle** (consumers > partitions).
77. Stop one active consumer. Rebalance — partitions migrate.
78. Add `partition.assignment.strategy="cooperative-sticky"`. Restart. Incremental rebalance.
79. Add `group.instance.id="c1"`, `c2`, etc. Restart within `session.timeout.ms`. **No rebalance** (static membership).

**Exit state:** Group parallelism, rebalance protocols, static membership observed.

---

### Phase 14 — Multiple consumer groups

**Trigger:** two unrelated systems need same data without sharing offsets.

**Goal:** Confirm group isolation.

80. Start consumers `group.id="analytics"` and `group.id="notifications"` on same topic.
81. Produce 100 messages. Both groups get all 100, independent committed offsets in AKHQ.

**Exit state:** Group isolation confirmed.

---

### Phase 15 — Multiple producers

**Trigger:** multiple services write to same topic.

**Goal:** Multi-producer ordering.

82. Run two producer scripts in parallel writing to `demo-p3` with overlapping keys.
83. Per partition, each producer's messages are ordered (with idempotence + `max.in.flight ≤ 5`); interleaving between producers is non-deterministic.
84. Distinct `transactional.id` per producer instance. Run both with transactions. No interference.

**Exit state:** Limits of ordering with multiple producers understood.

---

### Phase 16 — Multiple topics

**Trigger:** different event types should not share retention, schema, or access scope.

**Goal:** Topic design as deliberate decision.

85. Create `orders`, `payments`, `notifications` with naming convention `<domain>.<entity>.v1`.
86. Different retention per topic (`orders`: 7d, `notifications`: 1h).
87. One consumer subscribes to `["orders", "payments"]`. Gets partitions from both.
88. One consumer uses regex subscription `["^orders.*"]`. Create `orders.refunded` later, auto-included.
89. Rule of thumb: split topics when **schema, retention, access, or consumer shape** differ; otherwise add partitions.

**Exit state:** Topic design as first-class decision.

---

### Phase 17 — Observability: client metrics

**Goal:** See what producer/consumer do internally.

90. Producer: `statistics.interval.ms=5000` + `stats_cb` printing JSON. Read `record-send-rate`, `batch-size-avg`, `queue-len`, `outbuf-msg-cnt`.
91. Consumer: same. Read `records-lag-max`, `fetch-latency-avg`, `commit-latency-avg`.
92. From inside broker: `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group g1`. Read LAG per partition.

**Exit state:** Client-side health measurable.

---

### Phase 18 — Observability: broker metrics

**Goal:** See broker internals.

93. Compose: enable JMX (`KAFKA_JMX_PORT=9999`, `KAFKA_JMX_HOSTNAME=kafka`). Expose port. Restart.
94. Connect with `jmxterm` (or JConsole). Browse `kafka.server`, `kafka.network`, `kafka.log`.
95. Read: `BytesInPerSec`, `BytesOutPerSec`, `MessagesInPerSec`, `RequestsPerSec`, `TotalTimeMs` percentiles for `Produce` and `FetchConsumer`.
96. Add `prom/jmx-exporter` sidecar. Add Prometheus + Grafana services. Import standard Kafka dashboard (Grafana ID 7589 or similar).

**Exit state:** Broker health on dashboard.

---

### Phase 19 — Observability: tracing and logs

**Goal:** Trace one message end-to-end.

97. Producer adds header: `headers=[("trace_id", uuid4().hex.encode())]`. Log on send.
98. Consumer reads header, logs on receive. Grep one trace ID across both.
99. `docker logs <broker>`. Identify lines for: startup, topic creation, group rebalance.
100. Define minimal SLOs for single-broker setup: max consumer lag, producer error rate, broker disk %, broker uptime.

**Exit state:** End-to-end visibility.

---

### Phase 20 — Production patterns

**Goal:** Patterns that work on single broker and transfer to multi-broker later.

101. Add `confluentinc/cp-schema-registry` to compose. Register Avro schema for `orders`.
102. Switch producer to `SerializingProducer` + `AvroSerializer`. Consumer to `DeserializingConsumer` + `AvroDeserializer`. Schema fetched by ID.
103. Evolve schema (add optional field, BACKWARD compatible). Old consumer keeps working.
104. **Dead Letter Queue:** consumer catches deserialization errors, produces raw bytes to `orders.DLQ`, commits, moves on.
105. **Outbox pattern:** write to Postgres `outbox` table inside same DB transaction as business write. Separate relay polls `outbox` and produces to Kafka.
106. **Retry topic:** on processing failure, produce to `orders.retry.5s` with `not_before` header. Dedicated consumer waits then re-processes.
107. **Poison-pill handling:** track failed offsets; after N retries route to DLQ and commit past it.
108. **Event sourcing:** treat `orders` as source of truth. Build read model by replaying from offset 0 on consumer startup.

**Exit state:** Real-world patterns implemented.

---

### Phase 21 — Boundary (deferred — needs multi-broker)

Awareness only, do not attempt on single broker:

- Replication factor, leader/follower, ISR.
- `min.insync.replicas` × `acks=all`.
- Unclean leader election.
- Partition reassignment across brokers.
- Rack awareness.
- MirrorMaker 2 and DR topologies.
- Multi-broker capacity planning.
- KRaft controller failover (visible only with multiple controllers).

---

## Resume instructions for Claude

When the user says "I am at Phase X, Step N":

1. Treat the exit state of Step N-1 as the current state.
2. Do not re-explain prior steps unless asked.
3. Provide what is needed to complete Step N: exact commands, exact code, expected output, verification step.
4. Follow all rules in the "Rules for Claude" section above.
5. After Step N is verified, stop. Wait for user to confirm before moving to Step N+1.

---

## Progress tracker (user fills in)

```
[ ] Phase 0: Steps 1–9
[ ] Phase 1: Steps 10–15
[ ] Phase 2: Steps 16–25
[ ] Phase 3: Steps 26–31
[ ] Phase 4: Steps 32–35
[ ] Phase 5: Steps 36–41
[ ] Phase 6: Steps 42–47
[ ] Phase 7: Steps 48–51
[ ] Phase 8: Steps 52–54
[ ] Phase 9: Steps 55–58
[ ] Phase 10: Steps 59–63
[ ] Phase 11: Steps 64–67
[ ] Phase 12: Steps 68–72
[ ] Phase 13: Steps 73–79
[ ] Phase 14: Steps 80–81
[ ] Phase 15: Steps 82–84
[ ] Phase 16: Steps 85–89
[ ] Phase 17: Steps 90–92
[ ] Phase 18: Steps 93–96
[ ] Phase 19: Steps 97–100
[ ] Phase 20: Steps 101–108
```
