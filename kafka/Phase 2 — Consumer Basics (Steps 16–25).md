# Phase 2 — Consumer Basics (Steps 16–25)

## What I learned

A Kafka consumer reads messages from a topic. Two configs are mandatory:
- `bootstrap.servers` — where Kafka is.
- `group.id` — the consumer's "bookmark name."

### The bookmark analogy

`group.id` is a bookmark Kafka stores on the broker. It tracks how far this group has read in each partition.

- **Same `group.id`** across multiple consumers = they share the work. Each message goes to only one of them.
- **Different `group.id`** = each group gets its own independent copy of every message.

This is why Kafka is not a regular queue. A queue deletes a message after one read. Kafka keeps the message and lets every group read it independently.

### `auto.offset.reset` — only matters for new groups

This setting decides where the bookmark goes the **first time** a group connects.

| Value | Behavior |
|---|---|
| `latest` (default) | Start at the end of the log. Skip all existing messages. |
| `earliest` | Start at offset 0. Read everything from the beginning. |

**Critical rule:** `auto.offset.reset` is **only used when no committed offset exists** for the group. Once a group has committed even once, this setting is ignored on every future run.

If you want to replay from the start, you must either:
1. Use a new `group.id`.
2. Manually seek (Phase 8).
3. Reset offsets via CLI (Phase 8).

### Default auto-commit

`enable.auto.commit=true` and `auto.commit.interval.ms=5000` by default. The client commits the consumer's progress to Kafka every 5 seconds in the background. You did not call commit explicitly — it just happened.

---

## Files created

- `018_consume_g1.py` — minimum consumer: `bootstrap.servers`, `group.id="g1"`. Subscribed to `demo`. Polls in a loop.
- `022_consume_g2_earliest.py` — same as above but `group.id="g2"` and `auto.offset.reset="earliest"`.

## Observations

- `g1` (default `latest`) on first connect → printed nothing. Topic had 85 messages but they were skipped.
- After producing one new message, `g1` printed exactly that one (offset 84). Confirmed `latest` behavior.
- `g2` with `earliest` on first connect → printed all 85 messages from offset 0 to 84. Confirmed `earliest` behavior.
- Restarting `g2` with same code → printed nothing. Confirmed `auto.offset.reset` is ignored once a committed offset exists.
- AKHQ Consumer Groups view: `g1` and `g2` both at offset 85, lag 0. State `Empty` when no consumer running.

## Key facts to remember

1. Consumer groups are **state on the broker**, stored in internal topic `__consumer_offsets`. They survive consumer restarts.
2. Lag = End Offset − Current Offset. Zero means caught up. Most important operational metric.
3. A consumer that prints nothing usually does **not** mean the topic is empty — it means the bookmark is past the latest message.
4. Consumers are pull-based. `poll(timeout)` asks the broker; broker never pushes.
5. A Kafka consumer never exits at "end of log." It waits forever for new messages. Long-running service, not batch script.

## Environment state at end of Phase 2

- Topic `demo`: 1 partition, 85 messages (offsets 0–84).
- Consumer groups on broker: `g1` (offset 85, lag 0), `g2` (offset 85, lag 0).
- All containers still running: `kafka`, `akhq`, `python-dev`, `streaming-gateway`.