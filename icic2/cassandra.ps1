# ── Create Keyspace & Tables ─────────────────────────────────────────────────
docker exec -it etl-cassandra cqlsh


CREATE KEYSPACE IF NOT EXISTS etl
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS etl.text_events (
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

CREATE TABLE IF NOT EXISTS etl.image_events (
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
docker exec etl-cassandra cqlsh -k etl -e "DESCRIBE TABLES;"

# ── Full DDL (columns, types, primary key) ────────────────────────────────────
docker exec etl-cassandra cqlsh -e "DESCRIBE TABLE etl.text_events;"
docker exec etl-cassandra cqlsh -e "DESCRIBE TABLE etl.image_events;"

# ── Column List from System Schema ───────────────────────────────────────────
docker exec etl-cassandra cqlsh -e " SELECT column_name, type, kind FROM system_schema.columns WHERE keyspace_name = 'etl' AND table_name = 'text_events';"

docker exec etl-cassandra cqlsh -e " SELECT column_name, type, kind FROM system_schema.columns WHERE keyspace_name = 'etl' AND table_name = 'image_events';"

# ── Row Count ─────────────────────────────────────────────────────────────────
docker exec etl-cassandra cqlsh -e "SELECT COUNT(*) FROM etl.text_events;"
docker exec etl-cassandra cqlsh -e "SELECT COUNT(*) FROM etl.image_events;"

# ── Select Rows (truncated columns, wide terminal) ────────────────────────────
docker exec -e COLUMNS=220 etl-cassandra cqlsh -e " SELECT event_id, source, language, category, word_count, ingested_at FROM etl.text_events;"

docker exec -e COLUMNS=220 etl-cassandra cqlsh -e " SELECT event_id, source, image_id, format, size_bytes, lat, lon, ingested_at FROM etl.image_events;"