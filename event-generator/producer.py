import csv, random, uuid, time
from datetime import datetime, timedelta
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

users = [random.randint(100000, 999999) for _ in range(500)]
songs = [random.randint(1000, 99999) for _ in range(1000)]
regions = ["us", "eu", "apac"]
devices = ["ios", "mac", "web"]
events = ["play", "pause", "stop"]

while True:
    event = {
        "event_id": str(uuid.uuid4()),
        "user_id": random.choice(users),
        "song_id": random.choice(songs),
        "event_type": random.choices(events, [0.6, 0.25, 0.15])[0],
        "ts": datetime.utcnow().isoformat(),
        "device": random.choice(devices),
        "region": random.choice(regions)
    }
    producer.send("music_events", event)
    print(f"Sent to music_events topic: {event}")
    time.sleep(1)