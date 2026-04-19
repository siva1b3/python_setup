# ── Create Keyspace & Tables ─────────────────────────────────────────────────
docker exec -it svcd7 cqlsh


CREATE KEYSPACE IF NOT EXISTS ksvx
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS ksvx.text_events (
    event_id    text PRIMARY KEY,
    event_time  timestamp,
    source      text,
    language    text,
    category    text,
    title       text,
    content     text,
    word_count  int,
    tags        set<text>,
    ingested_at timestamp
);

CREATE TABLE IF NOT EXISTS ksvx.image_events (
    event_id    text PRIMARY KEY,
    event_time  timestamp,
    source      text,
    image_id    text,
    file_path   text,
    format      text,
    size_bytes  bigint,
    lat         double,
    lon         double,
    tags        set<text>,
    ingested_at timestamp
);


# ── List All Tables in Keyspace ───────────────────────────────────────────────
docker exec svcd7 cqlsh -k ksvx -e "DESCRIBE TABLES;"

# ── Full DDL (columns, types, primary key) ────────────────────────────────────
docker exec svcd7 cqlsh -e "DESCRIBE TABLE ksvx.text_events;"
docker exec svcd7 cqlsh -e "DESCRIBE TABLE ksvx.image_events;"

# ── Column List from System Schema ───────────────────────────────────────────
docker exec svcd7 cqlsh -e " SELECT column_name, type, kind FROM system_schema.columns WHERE keyspace_name = 'ksvx' AND table_name = 'text_events';"

docker exec svcd7 cqlsh -e " SELECT column_name, type, kind FROM system_schema.columns WHERE keyspace_name = 'ksvx' AND table_name = 'image_events';"

# ── Row Count ─────────────────────────────────────────────────────────────────
docker exec svcd7 cqlsh -e "SELECT COUNT(*) FROM ksvx.text_events;"
docker exec svcd7 cqlsh -e "SELECT COUNT(*) FROM ksvx.image_events;"

# ── Select Rows (truncated columns, wide terminal) ────────────────────────────
docker exec -e COLUMNS=220 svcd7 cqlsh -e " SELECT event_id, source, language, category, word_count, ingested_at FROM ksvx.text_events;"

docker exec -e COLUMNS=220 svcd7 cqlsh -e " SELECT event_id, source, image_id, format, size_bytes, lat, lon, ingested_at FROM ksvx.image_events;"
