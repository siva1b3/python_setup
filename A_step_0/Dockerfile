FROM python:3.14-slim-bookworm

# Install uv package manager
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install dependencies first (cached layer unless pyproject.toml changes)
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync

# Copy application code
COPY simulator.py .

# ── BURST MODE ───────────────────────────────────────────
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "10", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "100", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "1000", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "5000", "--dry-run"]

# ── STREAM MODE ──────────────────────────────────────────
CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "1", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "5", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "10", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "50", "--dry-run"]

# ── SEND TO API (Step 1+) ───────────────────────────────
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "100", "--target", "http://localhost:8000/api/events/"]
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "5", "--target", "http://localhost:8000/api/events/"]

# ── DRY RUN (no API, print only) ────────────────────────
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "10", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "1000", "--dry-run"]
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "5", "--dry-run"]

# ── BURST TO API ────────────────────────────────────────
# Quick smoke test — 10 events
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "10", "--target", "http://flightdeck-dev:8000/api/events/"]

# Step 2 — verify persistence across restart
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "100", "--target", "http://flightdeck-dev:8000/api/events/"]

# Step 4 — stress test baseline
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "1000", "--target", "http://flightdeck-dev:8000/api/events/"]

# Step 4 — find the breaking point
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "5000", "--target", "http://flightdeck-dev:8000/api/events/"]

# Step 9 — push PostgreSQL to limits
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "50000", "--target", "http://flightdeck-dev:8000/api/events/"]

# ── STREAM TO API ───────────────────────────────────────
# Slow — watch logs in Dozzle (Step 5+)
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "1", "--target", "http://flightdeck-dev:8000/api/events/"]

# Normal — steady load for consumer testing (Step 6+)
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "5", "--target", "http://flightdeck-dev:8000/api/events/"]

# Fast — consumer lag testing (Step 7+)
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "10", "--target", "http://flightdeck-dev:8000/api/events/"]

# Heavy — Grafana dashboard under load (Step 8+)
# CMD ["uv", "run", "simulator.py", "--mode", "stream", "--rate", "50", "--target", "http://flightdeck-dev:8000/api/events/"]

# Step 16 — end-to-end burst verification
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "6000", "--target", "http://flightdeck-dev:8000/api/events/"]

# Step 16 — burst 10k, no crashes, lag returns to 0
# CMD ["uv", "run", "simulator.py", "--mode", "burst", "--count", "10000", "--target", "http://flightdeck-dev:8000/api/events/"]

# ── KEEP ALIVE (for interactive use via docker exec) ─────
# CMD ["tail", "-f", "/dev/null"]


# ── KEEP ALIVE (for interactive use via docker exec) ─────
# CMD ["tail", "-f", "/dev/null"]