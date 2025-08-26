import psycopg2
import pandas as pd
import streamlit as st
import plotly.express as px
import os

# load data
POSTGRES_PORT=os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB=os.getenv("POSTGRES_DB", "musicdb")
POSTGRES_USER=os.getenv("POSTGRES_USER", "music")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD", "musicpw")
conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host="postgres",
    port=POSTGRES_PORT
)

df = pd.read_sql("SELECT * FROM daily_metrics ORDER BY day", conn)
conn.close()

st.title("Music App Daily Event Metrics")
# Select event type filter
event_type = st.selectbox("Select Event Type", df['event_type'].unique())
filtered_df = df[df['event_type'] == event_type]

# Line chart: events over time
fig = px.line(filtered_df, x="day", y="cnt", color="region", markers=True)
st.plotly_chart(fig)

# Show raw table
st.subheader("Raw Data")
st.dataframe(filtered_df)
