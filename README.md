# Music Streaming Data Pipeline

**Stack:** Python, Spark, Kafka, Postgres, Streamlit, Docker  

---

## Overview

This project simulates an **end-to-end data pipeline** for a music streaming service. It demonstrates:

- Streaming events for user interactions with music (play, pause, stop).  
- Batch processing and analytics using Spark.  
- Deduplication, staging, and upsert into Postgres.  
- Aggregation of daily metrics (events per day, per region).  
- Visualization using a simple Streamlit dashboard.  
- Fully containerized local setup with Docker Compose.

This project is designed as a **portfolio example for data engineering / analytics roles**, showing pipeline design, ETL, and analytics workflow.

---

## Project Architecture

CSV / Kafka → Spark (Batch + Streaming) → Postgres (raw + metrics) → Streamlit Dashboard



**Stages:**

1. **Data Generation / Kafka Producer**  
   - Generates synthetic user music events (`play`, `pause`, `stop`).  
   - Each event has: `event_id`, `user_id`, `event_type`, `region`, `ts`.  
   - Events can be written to CSV (batch) or pushed to **Kafka** (streaming).  

2. **Spark Batch ETL**  
   - Reads CSV events or Kafka micro-batches.  
   - Deduplicates events by `event_id`.  
   - Writes to **staging/raw tables** in Postgres.  
   - Aggregates **daily metrics** (day x event_type x region) and writes to `daily_metrics`.

3. **Spark Structured Streaming (Streaming ETL)**  
   - Consumes real-time events from Kafka (`music_events` topic).  
   - Parses JSON messages, deduplicates, and writes micro-batches to Postgres (`raw_events`).  
   - Computes **real-time daily metrics** using time windows and watermarks.  
   - Metrics can be written to Postgres for near real-time dashboard updates.

4. **Dashboard (Streamlit)**  
   - Connects to Postgres and loads `daily_metrics`.  
   - Displays interactive line charts per event type and region.  
   - Shows raw metrics table for transparency.  

5. **Containerization**  
   - Postgres for raw + metrics tables.  
   - Kafka + Zookeeper for streaming events.  
   - Streamlit for dashboard.  
   - Docker Compose ensures reproducible local environment.

---

## Local Setup

### Prerequisites

- Docker & Docker Compose installed  
- Python 3.10+ for local testing  

### Steps

1. Clone the repo:

```bash
git clone <repo-url>
cd music-streaming-pipeline
```

2. Build and run the stack
```bash
docker-compose up
```

3. Access the dashboard
```bash
http://localhost:8501
```

4. To run spark batch ETL locally:
```bash
spark-submit --jars jars/postgresql-42.7.3.jar spark/batch_etl.py
```
---

## Key Features Demonstrated

- End-to-End Pipeline: Event generation → Spark Batch/Streaming → Postgres → Dashboard
- Realistic Event Simulation: Weighted probabilities for play/pause/stop
- Batch + Streaming ETL: Deduplication, staging table, upsert into raw table
- Streaming Metrics: Real-time daily metrics aggregated by event type & region
- Visualization: Interactive dashboard with Streamlit
- Containerized: Fully reproducible local environment using Docker Compose