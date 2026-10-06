"""
Online Feature Store Extractor
Extracts sliding window aggregates and online serving features for low-latency retrieval.
"""
import pandas as pd
from datetime import datetime, timezone

def extract_online_features(events):
    df = pd.DataFrame(events)
    if df.empty:
        return []
    
    feature_records = []
    grouped = df.groupby("user_id")
    
    now = datetime.now(timezone.utc).isoformat()
    
    for user_id, group in grouped:
        total_tokens = int(group["total_tokens"].sum())
        avg_latency = round(float(group["latency_ms"].mean()), 2)
        avg_similarity = round(float(group["vector_similarity_score"].mean()), 4)
        dominant_model = group["model_id"].mode()[0]
        event_count = len(group)
        
        feature_records.append({
            "entity_id": user_id,
            "feature_set": "user_online_profile",
            "rolling_tokens_1h": total_tokens,
            "avg_latency_ms": avg_latency,
            "avg_vector_similarity": avg_similarity,
            "preferred_model": dominant_model,
            "recent_request_count": event_count,
            "last_updated_at": now
        })
        
    return feature_records
