docker compose exec kafka kafka-topics --create \
  --topic music-events --partitions 1 --replication-factor 1 \
  --bootstrap-server kafka:9092