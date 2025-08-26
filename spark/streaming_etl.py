from pyspark.sql import SparkSession, functions as F

spark = (spark.SparkSession.builder
            .appName("MusicStreamingETL")
            .getOrCreate())

# read from Kafka
df = (spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "music_events")
        .load()    
    )

# transform data from binary (kafka type) to structured column (for Spark processing)
events = (
    df.selectExpr("cast(value as string) as json")
        .select(F.from_json("json", """
            event_id STRING,
            user_id STRING,
            song_id STRING,
            region STRING,
            event_type STRING,
            device STRING,
            ts STRING
        """).alias("data"))
        .select("data.*")
        .withColumn("ts", F.to_timestamp("ts"))
)

dedup = events.dropDuplicates(["event_id"])

POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB=os.getenv("POSTGRES_DB", "musicdb")
POSTGRES_USER=os.getenv("POSTGRES_USER", "music")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "musicpw")
pg_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# write to postgres-append
(dedup.writeStream
    .foreachBatch(lambda batch_df, _: (
        batch_df.write
            .format("jdbc")
            .option("url", pg_url)
            .option("dbtable", "raw_events")
            .option("user", POSTGRES_USER)
            .option("password", POSTGRES_PASSWORD)
            .mode("append")
            .save()
    ))
    .outputMode("update")
    .start()
    .awaitTermination()
)