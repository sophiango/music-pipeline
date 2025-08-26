# Music Streaming Data Pipeline

**Stack:** Python, Spark, Kafka (simulated), Postgres, Streamlit, Docker  

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

CSV / Simulated Kafka → Spark Batch ETL → Postgres (raw + metrics) → Streamlit Dashboard


**Stages:**

1. **Data Generation**  
   - Generates synthetic user music events (`play`, `pause`, `stop`).  
   - Each event has: `event_id`, `user_id`, `event_type`, `region`, `ts`.  
   - Events are distributed realistically over the day.  

2. **Spark ETL**  
   - Reads events CSV (or Kafka stream).  
   - Deduplicates events by `event_id`.  
   - Writes to **staging table** in Postgres.  
   - Upserts into **raw_events** table using Postgres SQL (`ON CONFLICT DO NOTHING`).  
   - Aggregates **daily metrics**: `day x event_type x region`.  
   - Writes metrics to `daily_metrics` table.

3. **Dashboard (Streamlit)**  
   - Connects to Postgres and loads `daily_metrics`.  
   - Displays interactive line charts per event type and region.  
   - Shows raw metrics table for transparency.  

4. **Containerization**  
   - Postgres service for raw + metrics tables.  
   - Streamlit service for dashboard.  
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

## Folder structure
```bash
music-streaming-pipeline/
├─ data/                  # Sample CSV or generated data
├─ spark/
│   └─ batch_etl.py       # ETL pipeline code
├─ dashboard/
│   └─ dashboard.py       # Streamlit dashboard
├─ jars/
│   └─ postgresql-42.7.3.jar  # JDBC driver
├─ docker-compose.yml
└─ README.md
```
---

## Key Features Demonstrated
End-to-End Pipeline: Event generation → Spark → Postgres → Dashboard
Realistic Event Simulation: Weighted probabilities for play/pause/stop
ETL Best Practices: Deduplication, staging table, upsert into raw table
Analytics Layer: Daily metrics aggregated by event type and region
Visualization: Interactive dashboard with Streamlit
Containerized: Fully reproducible local environment using Docker Compose

