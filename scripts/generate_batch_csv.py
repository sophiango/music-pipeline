import csv, random, uuid, time
from datetime import datetime, timedelta

users = [random.randint(100000, 999999) for _ in range(500)]
songs = [random.randint(1000, 99999) for _ in range(1000)]
regions = ["us", "eu", "apac"]
devices = ["ios", "mac", "web"]
events = ["play", "pause", "stop"]

rows=[]
start = datetime.now() - timedelta(days=3)
for d in range(3):
    day = start + timedelta(days=d)
    for _ in range(10000):
        # this pick play/pause/stop with 60% probability will be play, 25% pause and 15% stop, simulate more realistic user's behavior
        choice_event = random.choices(events, [0.6, 0.25, 0.15])[0]
        rows.append({
            "event_id": str(uuid.uuid4()),
            "user_id": random.choice(users),
            "song_id": random.choice(songs),
            "event_type": choice_event,
            "ts": (day + timedelta(seconds=random.randint(0,86400))).isoformat(),
            "device": random.choice(devices),
            "region": random.choice(regions)
        })

with open("data/events.csv", "w", newline="") as f:
    w = csv.DictWriter(f,fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)

print("Successfully wrote to data/events.csv")