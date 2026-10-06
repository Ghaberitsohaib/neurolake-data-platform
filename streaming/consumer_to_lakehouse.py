"""
Kafka Consumer to Partitioned MinIO/Parquet Lakehouse Sink
Target: Bronze Lakehouse & DuckDB Landing Schema
"""
import os
import duckdb
import pandas as pd
from datetime import datetime, timezone
from streaming.producer_ai_events import produce_stream
from streaming.real_time_feature_extractor import extract_online_features

def sink_stream_to_lakehouse(batch_size=60):
    lake_dir = os.path.join(os.path.dirname(__file__), "..", "data_lake", "bronze", "inference")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "neurolake_warehouse.duckdb")
    os.makedirs(lake_dir, exist_ok=True)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    print(f"[Streaming Consumer] Ingesting {batch_size} AI inference telemetry events...")
    events = produce_stream(batch_size)
    online_features = extract_online_features(events)
    
    df_inference = pd.DataFrame(events)
    df_features = pd.DataFrame(online_features)

    # 1. Partitioned Lakehouse Parquet Sink
    now = datetime.now(timezone.utc)
    part_dir = os.path.join(lake_dir, f"year={now.year}", f"month={now.month:02d}", f"day={now.day:02d}")
    os.makedirs(part_dir, exist_ok=True)
    parquet_path = os.path.join(part_dir, f"ai_inference_{int(now.timestamp())}.parquet")
    df_inference.to_parquet(parquet_path, index=False, engine="pyarrow")

    # 2. Sync to DuckDB Raw Landing
    con = duckdb.connect(db_path, read_only=False)
    con.execute("CREATE SCHEMA IF NOT EXISTS neurolake_raw;")
    con.execute("CREATE OR REPLACE TABLE neurolake_raw.ai_inference_events AS SELECT * FROM df_inference;")
    con.execute("CREATE OR REPLACE TABLE neurolake_raw.online_features AS SELECT * FROM df_features;")
    con.close()

    print(f"[Lakehouse Sink] Successfully landed {len(df_inference)} events to Parquet & DuckDB!")

if __name__ == "__main__":
    sink_stream_to_lakehouse(50)
