docker exec -it etl-cassandra cqlsh -e "
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
"