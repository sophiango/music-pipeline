from pyspark.sql import SparkSession, functions as F
import os
import psycopg2

POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB=os.getenv("POSTGRES_DB", "musicdb")
POSTGRES_USER=os.getenv("POSTGRES_USER", "music")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "musicpw")
pg_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
pg_props = {
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
    "driver": "org.postgresql.Driver"
}
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)
cur = conn.cursor()

spark = (SparkSession.builder
        .appName("music-batch-etl")
        .config("spark.jars.package", "org.postgresql:postgresql:42.7.3")
        .getOrCreate())

df = (spark.read.option("header", True).csv("data/events.csv")
    .withColumn("ts", F.to_timestamp("ts"))
    .filter(F.col("event_type").isin("play", "pause", "stop")))

# write new data into staging table temp
raw = df.dropDuplicates(["event_id"])
(raw.write
    .format("jdbc").mode("overwrite") # replace all events in staging each time this run
    .option("url", pg_url)
    .option("dbtable", "staging_events")
    .options(**pg_props)
    .save())

# upsert to raw event
cur.execute("""
    INSERT INTO raw_events (event_id, user_id, event_type, region, ts)
    SELECT event_id, user_id, event_type, region, ts
    FROM staging_events
    ON CONFLICT (event_id) DO NOTHING;
""")
conn.commit()
cur.close()
conn.close()

daily = (spark.read.format("jdbc")
    .option("url", pg_url)
    .option("dbtable", "raw_events")
    .options(**pg_props)
    .load()
    .withColumn("day", F.to_date("ts"))
    .groupBy("day", "event_type", "region")
    .agg(F.count("*").alias("cnt")))

# write to daily metrics
(daily.write
    .format("jdbc").mode("append")
    .option("url", pg_url)
    .option("dbtable", "daily_metrics")
    .options(**pg_props)
    .save())