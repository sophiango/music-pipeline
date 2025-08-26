docker compose exec -T postgres psql -U music -d musicdb <<'SQL'
CREATE TABLE IF NOT EXISTS raw_events(
  event_id text PRIMARY KEY, user_id text, song_id text, event_type text,
  ts timestamptz, device text, region text
);
CREATE TABLE IF NOT EXISTS staging_events(
  event_id text PRIMARY KEY, user_id text, song_id text, event_type text,
  ts timestamptz, device text, region text
);
CREATE TABLE IF NOT EXISTS daily_metrics(
  day date, event_type text, region text, cnt bigint, UNIQUE(day,event_type,region)
);
SQL
