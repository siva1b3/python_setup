"""
FlightDeck Event Simulator

Generates synthetic aerospace operational events for testing.

Usage:
    # ── SETUP (first time only) ──────────────────────────────
    uv sync

    # ── BURST MODE ───────────────────────────────────────────

    # Quick test — 10 events, print only
    uv run simulator.py --mode burst --count 10 --dry-run

    # Medium test — verify 70/20/10 distribution
    uv run simulator.py --mode burst --count 100 --dry-run

    # Distribution validation — 1000 events
    uv run simulator.py --mode burst --count 1000 --dry-run

    # Large burst — 5000 events (used in Step 4 for stress testing)
    uv run simulator.py --mode burst --count 5000 --dry-run

    # Send to API (Step 1+)
    uv run simulator.py --mode burst --count 100 --target http://localhost:8000/api/events/
    uv run simulator.py --mode burst --count 1000 --target http://localhost:8000/api/events/
    uv run simulator.py --mode burst --count 5000 --target http://localhost:8000/api/events/

    # ── STREAM MODE ──────────────────────────────────────────

    # Slow stream — 1 event/sec, good for watching logs
    uv run simulator.py --mode stream --rate 1 --dry-run

    # Default stream — 5 events/sec
    uv run simulator.py --mode stream --rate 5 --dry-run

    # Fast stream — 10 events/sec
    uv run simulator.py --mode stream --rate 10 --dry-run

    # Heavy stream — 50 events/sec (Step 4+ stress testing)
    uv run simulator.py --mode stream --rate 50 --dry-run

    # Stream to API (Step 1+)
    uv run simulator.py --mode stream --rate 5 --target http://localhost:8000/api/events/
    uv run simulator.py --mode stream --rate 10 --target http://localhost:8000/api/events/

    # ── VERIFY ───────────────────────────────────────────────

    # Single event — inspect full JSON
    uv run python -c "from simulator import generate_event; import json; print(json.dumps(generate_event(), indent=2))"
"""

import argparse
import json
import random
import sys
import time
from datetime import datetime, timezone

import requests
from faker import Faker

fake = Faker()

# ---------------------------------------------------------------------------
# Source system definitions
# ---------------------------------------------------------------------------

SOURCE_SYSTEMS = {
    "propulsion-monitor": {
        "messages": {
            "INFO": [
                "Engine start successful",
                "Thrust nominal",
                "Fuel flow stable",
            ],
            "WARN": [
                "Vibration above normal",
                "Fuel consumption high",
            ],
            "ERROR": [
                "Hydraulic pressure exceeded threshold",
                "Engine overheat detected",
                "Thrust vectoring failure",
            ],
        },
        "metadata": lambda: {
            "sensor_id": f"HYD-{random.randint(1, 99):03d}",
            "reading": round(random.uniform(2000, 4000), 1),
            "threshold": 3000,
            "unit_id": f"aircraft-{random.randint(1, 20)}",
            "engine_number": random.randint(1, 4),
        },
    },
    "nav-system": {
        "messages": {
            "INFO": [
                "GPS lock acquired",
                "Waypoint reached",
                "Altitude stable",
            ],
            "WARN": [
                "GPS signal degraded",
                "Heading drift detected",
            ],
            "ERROR": [
                "GPS lock lost",
                "INS alignment failure",
                "Altitude deviation critical",
            ],
        },
        "metadata": lambda: {
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6),
            "altitude": round(random.uniform(0, 45000), 1),
            "heading": round(random.uniform(0, 360), 1),
            "speed": round(random.uniform(0, 900), 1),
            "satellite_count": random.randint(0, 24),
        },
    },
    "comms-relay": {
        "messages": {
            "INFO": [
                "Uplink established",
                "Telemetry transmitted",
                "Handoff complete",
            ],
            "WARN": [
                "Signal strength low",
                "Latency above threshold",
            ],
            "ERROR": [
                "Uplink lost",
                "Telemetry gap detected",
                "Frequency interference",
            ],
        },
        "metadata": lambda: {
            "frequency": round(random.uniform(100, 2400), 2),
            "signal_strength_dbm": round(random.uniform(-120, -30), 1),
            "link_id": f"LINK-{random.randint(1, 50):03d}",
            "bandwidth_kbps": random.choice([64, 128, 256, 512, 1024]),
        },
    },
    "thermal-control": {
        "messages": {
            "INFO": [
                "Coolant flow nominal",
                "Bay temperature stable",
            ],
            "WARN": [
                "Temperature approaching limit",
                "Coolant pressure low",
            ],
            "ERROR": [
                "Thermal runaway detected",
                "Coolant system failure",
                "Sensor malfunction",
            ],
        },
        "metadata": lambda: {
            "sensor_id": f"THERM-{random.randint(1, 60):03d}",
            "temperature_c": round(random.uniform(-40, 150), 1),
            "zone": random.choice(["bay-1", "bay-2", "bay-3", "engine-nacelle", "avionics"]),
            "coolant_flow_rate": round(random.uniform(0.5, 15.0), 2),
        },
    },
    "power-distribution": {
        "messages": {
            "INFO": [
                "Bus voltage nominal",
                "Battery charged",
                "Load balanced",
            ],
            "WARN": [
                "Voltage fluctuation detected",
                "Battery below 30%",
            ],
            "ERROR": [
                "Bus fault detected",
                "Generator offline",
                "Load shedding activated",
            ],
        },
        "metadata": lambda: {
            "bus_id": f"BUS-{random.choice(['A', 'B', 'C', 'D'])}{random.randint(1, 4)}",
            "voltage": round(random.uniform(24, 32), 2),
            "current_amps": round(random.uniform(0, 200), 1),
            "load_percentage": round(random.uniform(10, 100), 1),
        },
    },
}

EVENT_TYPE_WEIGHTS = {
    "INFO": 0.70,
    "WARN": 0.20,
    "ERROR": 0.10,
}

# ---------------------------------------------------------------------------
# Event generation
# ---------------------------------------------------------------------------


def pick_event_type() -> str:
    return random.choices(
        population=list(EVENT_TYPE_WEIGHTS.keys()),
        weights=list(EVENT_TYPE_WEIGHTS.values()),
        k=1,
    )[0]


def generate_event() -> dict:
    source = random.choice(list(SOURCE_SYSTEMS.keys()))
    system = SOURCE_SYSTEMS[source]
    event_type = pick_event_type()
    message = random.choice(system["messages"][event_type])
    metadata = system["metadata"]()

    return {
        "source_system": source,
        "event_type": event_type,
        "message": message,
        "metadata": metadata,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

# Pad source names to fixed width for aligned console output
_MAX_SOURCE_LEN = max(len(s) for s in SOURCE_SYSTEMS)


def format_event_line(index: int, event: dict) -> str:
    source = event["source_system"].ljust(_MAX_SOURCE_LEN)
    etype = event["event_type"].ljust(5)
    meta_short = json.dumps(event["metadata"], separators=(",", ":"))
    if len(meta_short) > 60:
        meta_short = meta_short[:57] + "..."
    return f"[{index:04d}] {etype} {source} | {event['message']} | {meta_short}"


def print_summary(counters: dict[str, int], total: int) -> None:
    parts = " | ".join(f"{k}: {v}" for k, v in sorted(counters.items()))
    print(f"\nSummary: {total} events | {parts}")


def send_event(target: str, event: dict) -> bool:
    """POST event to target URL. Returns True on success."""
    try:
        resp = requests.post(target, json=event, timeout=5)
        return resp.status_code in (200, 201, 202)
    except requests.RequestException as exc:
        print(f"  [SEND FAILED] {exc}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------


def run_burst(count: int, target: str | None, dry_run: bool) -> None:
    counters: dict[str, int] = {"INFO": 0, "WARN": 0, "ERROR": 0}
    failed = 0

    for i in range(1, count + 1):
        event = generate_event()
        counters[event["event_type"]] += 1
        print(format_event_line(i, event))

        if not dry_run and target:
            if not send_event(target, event):
                failed += 1

    print_summary(counters, count)
    if failed:
        print(f"Failed to send: {failed}/{count}")


def run_stream(rate: float, target: str | None, dry_run: bool) -> None:
    interval = 1.0 / rate
    counters: dict[str, int] = {"INFO": 0, "WARN": 0, "ERROR": 0}
    total = 0
    failed = 0

    print(f"Streaming at {rate} events/sec (Ctrl+C to stop)\n")

    try:
        while True:
            event = generate_event()
            total += 1
            counters[event["event_type"]] += 1
            print(format_event_line(total, event))

            if not dry_run and target:
                if not send_event(target, event):
                    failed += 1

            time.sleep(interval)
    except KeyboardInterrupt:
        pass

    print_summary(counters, total)
    if failed:
        print(f"Failed to send: {failed}/{total}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="FlightDeck Event Simulator")
    parser.add_argument(
        "--mode",
        choices=["burst", "stream"],
        required=True,
        help="burst = generate N events; stream = continuous at fixed rate",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of events (burst mode only, default: 100)",
    )
    parser.add_argument(
        "--rate",
        type=float,
        default=5.0,
        help="Events per second (stream mode only, default: 5)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=None,
        help="URL to POST events to (e.g. http://localhost:8000/api/events/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print events only, do not send",
    )

    args = parser.parse_args()

    if args.mode == "burst":
        run_burst(args.count, args.target, args.dry_run)
    else:
        run_stream(args.rate, args.target, args.dry_run)


if __name__ == "__main__":
    main()