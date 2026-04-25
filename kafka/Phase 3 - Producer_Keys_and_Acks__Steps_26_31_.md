# Phase 3 — Producer: Keys and Acknowledgements (Steps 26–31)

## What I learned

Phase 3 added two producer concepts: **message keys** (Steps 26–27) and **delivery acknowledgements** (Steps 28–31). The end of this phase produced the standard producer template used for the rest of the roadmap.

### Message keys

A Kafka message has these parts: `key`, `value`, `headers`, `timestamp`, plus broker-assigned `partition` and `offset`. The key is optional metadata attached to each message.

Keys do two things:
1. **Routing** — when a topic has multiple partitions, Kafka hashes the key to pick a partition. Same key → same partition, always. Guarantees per-key ordering.
2. **Identity** — log compaction (Phase 11) uses the key to decide which messages to keep.

**On a 1-partition topic, keys are stored but do not route anywhere.** Every message goes to partition 0 regardless of key. The hash is computed but discarded because `hash % 1 = 0`. This is why keys appear meaningless in Phase 3 — their real effect appears in Phase 12 (multi-partition).

### Delivery callbacks

`producer.produce()` is **non-blocking and asynchronous**. It does not send the message immediately. It places the message into an internal queue inside `librdkafka`. A background thread batches and sends.

Timeline:
```
your code: producer.produce(...)        → returns immediately
librdkafka thread: batches message
librdkafka thread: sends batch to broker
broker:           writes to log, returns ack
librdkafka thread: receives ack
librdkafka thread: invokes your callback
```

Two key facts about the callback:
1. **`produce()` does not send the message.** It only queues. That is why `print` after `produce()` runs immediately.
2. **The callback runs only when you call `flush()` or `poll()`.** The library does not spawn a Python thread to invoke callbacks. They are queued and delivered when the main thread asks.

Callback signature: `def callback(err, msg)`.
- `err` = `None` on success, `KafkaError` on failure.
- `msg` = `Message` object with `.topic()`, `.partition()`, `.offset()`, `.key()`, `.value()`, `.timestamp()`.

### `acks` — producer's safety contract

`acks` controls how many confirmations the producer waits for before considering a message "successfully sent."

| `acks` | Waits for | On single broker | On 3-broker cluster |
|---|---|---|---|
| `0` | Nothing | No confirmation, callback offset is `None` | No confirmation |
| `1` | Leader only | Real offset returned | Risk of loss if leader dies before replication |
| `all` (`-1`) | Leader + all ISR | Same as `acks=1` (no other replicas exist) | Safe across single-broker failures |

**Critical point about `acks=0`:** The callback still fires and reports "OK", but `msg.offset()` returns `None`. This is the producer's blind spot — it has no way to know if the broker accepted the message. On a healthy single broker the messages do arrive (visible in AKHQ with real offsets), but the producer never learns those offsets. In a real failure scenario this is **silent data loss**.

**Why `acks=all` is the production default:**
- Only setting that survives single-broker failure in a multi-broker cluster.
- Required by `enable.idempotence=true` (Step 36).
- Already the default in modern `librdkafka`, but writing it explicitly makes the contract self-documenting and protects against future default changes.

### `acks=all` on single broker

With one broker, the ISR contains only the leader itself. So `acks=all` waits for one broker, identical to `acks=1` in observable behavior. The difference only appears in multi-broker setups (Phase 21, deferred).

---

## Files created

- `026_produce_with_key.py` — single message with `key="user-1"`. Confirmed key column populated in AKHQ.
- `027_produce_two_keys.py` — 5 messages with `user-1`, 5 with `user-2`. Confirmed all 10 land in partition 0 on a 1-partition topic.
- `028_produce_with_callback.py` — added `on_delivery` callback. Observed `produce() returned` lines printing before any `OK:` lines, proving callbacks fire only during `flush()`.
- `029_produce_acks_1.py` — explicit `acks=1`. Real offsets in callback. No behavioral change vs. default.
- `030_produce_acks_0.py` — `acks=0`. Callback printed `offset=None` for all three messages. Messages still appeared in AKHQ with real offsets (broker was healthy).
- `031_produce_acks_all.py` — `acks=all`. Real offsets returned. This is the producer template used going forward.

## Observations

- **Step 26:** `key="user-1"` appeared in AKHQ Key column. Previously empty. Partition still 0.
- **Step 27:** All 10 messages with two distinct keys went to partition 0. Confirms keys do not route on 1-partition topics.
- **Step 28:** Print statement order proved `produce()` is non-blocking:
  ```
  produce() returned for message 0
  produce() returned for message 1
  produce() returned for message 2
  calling flush()...
  OK: ... offset=96 key=user-0
  OK: ... offset=97 key=user-1
  OK: ... offset=98 key=user-2
  flush() returned
  ```
  All three "produce() returned" lines came first. Callbacks ran only during `flush()`.
- **Step 29:** `acks=1` produced real offsets. Same behavior as Step 28's default.
- **Step 30:** `acks=0` produced `offset=None` in callback. Verified in AKHQ that messages still arrived with real offsets — proving the producer's report is unreliable, not that messages are lost.
- **Step 31:** `acks=all` produced real offsets. No latency difference from `acks=1` on single broker. Adopted as standard config.

## Key facts to remember

1. **`produce()` is asynchronous.** Message goes into an internal queue, not directly to broker.
2. **Callbacks fire only during `flush()` or `poll()`.** They are not pushed to your code by background threads.
3. **`flush()` is mandatory before exit.** Without it, queued messages are lost when the script ends.
4. **Callback exceptions are swallowed by librdkafka.** Wrap risky code in try/except inside the callback.
5. **`msg.value()` and `msg.key()` return bytes in the callback,** not the original strings.
6. **`acks=0` is silent data loss territory.** Callback says "OK" but offset is `None` — producer has no proof.
7. **`acks=all` is the only setting safe for replicated production data.** Required for idempotence.
8. **Keys are always stored, even when routing is trivial.** They become meaningful with multiple partitions.
9. **Per-key ordering is guaranteed, but only within one partition.** Across partitions, no global order.
10. **In `confluent-kafka-python`, default `acks` is already `all`.** Writing it explicitly is for clarity, not behavior change.

## Producer template (carry forward)

This is the baseline producer config used from Step 31 onward:

```python
from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"FAILED: {err}")
        return
    print(
        f"OK: topic={msg.topic()} "
        f"partition={msg.partition()} "
        f"offset={msg.offset()} "
        f"key={msg.key().decode() if msg.key() else None}"
    )

producer = Producer({
    "bootstrap.servers": "kafka:29092",
    "acks": "all",
})

producer.produce(
    topic="demo",
    key="user-1",
    value="payload",
    on_delivery=delivery_report,
)

producer.flush()
```

## Comparison summary

| Step | acks | Callback offset | Messages in AKHQ |
|---|---|---|---|
| 28 | (default `all`) | real number | yes, real offsets |
| 29 | `1` | real number | yes, real offsets |
| 30 | `0` | `None` | yes (broker healthy), but producer has no proof |
| 31 | `all` | real number | yes, real offsets |

## Environment state at end of Phase 3

- Topic `demo`: 1 partition, ~110+ messages (offsets accumulated across all phases).
- Consumer groups on broker: `g1`, `g2` (both at lag 0, idle).
- All containers still running: `kafka`, `akhq`, `python-dev`, `streaming-gateway`.
- Standard producer config locked in: `bootstrap.servers` + `acks=all` + `on_delivery` callback.

## Deferred to Phase 21 (multi-broker)

- Real difference between `acks=1` and `acks=all` (requires replicas).
- ISR (In-Sync Replicas) behavior.
- `min.insync.replicas` interaction with `acks=all`.
- Leader failover and message survival.

---
