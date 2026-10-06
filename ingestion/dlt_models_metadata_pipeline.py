"""
dltHub Ingestion Pipeline for AI Model Registry and Feature Definitions
Target: Lakehouse landing schema (neurolake_raw)
"""
import os
import duckdb
import pandas as pd
from datetime import datetime, timezone

def run_dlt_metadata_ingestion():
    print("[dltHub] Starting AI Model Registry and Feature Metadata sync...")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "neurolake_warehouse.duckdb")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # 1. Registered Foundation Models & Pricing Tiers
    models_data = [
        {"model_id": "gpt-4o", "provider": "OpenAI", "category": "Multimodal LLM", "context_window": 128000, "prompt_cost_per_1k": 0.005, "completion_cost_per_1k": 0.015, "is_active": True},
        {"model_id": "claude-3-5-sonnet", "provider": "Anthropic", "category": "Advanced Reasoning", "context_window": 200000, "prompt_cost_per_1k": 0.003, "completion_cost_per_1k": 0.015, "is_active": True},
        {"model_id": "llama-3-70b-instruct", "provider": "Meta AI / Self-Hosted", "category": "Open-Weights LLM", "context_window": 8192, "prompt_cost_per_1k": 0.0009, "completion_cost_per_1k": 0.0009, "is_active": True},
        {"model_id": "mistral-large-2", "provider": "Mistral AI", "category": "Multilingual Enterprise", "context_window": 128000, "prompt_cost_per_1k": 0.002, "completion_cost_per_1k": 0.006, "is_active": True},
        {"model_id": "text-embedding-3-large", "provider": "OpenAI", "category": "Vector Embedding", "context_window": 8191, "prompt_cost_per_1k": 0.00013, "completion_cost_per_1k": 0.0, "is_active": True}
    ]
    df_models = pd.DataFrame(models_data)
    df_models["synced_at"] = datetime.now(timezone.utc).isoformat()

    # 2. Registered Online Feature Catalog
    features_catalog = [
        {"feature_name": "user_rolling_tokens_1h", "entity": "user_id", "data_type": "INT64", "freshness_sla_sec": 5, "description": "Total prompt tokens consumed in rolling 60 min window"},
        {"feature_name": "user_rag_avg_similarity", "entity": "user_id", "data_type": "FLOAT64", "freshness_sla_sec": 10, "description": "Average Cosine similarity of retrieved knowledge chunks"},
        {"feature_name": "session_latency_p90", "entity": "session_id", "data_type": "FLOAT64", "freshness_sla_sec": 15, "description": "90th percentile response latency in current active session"},
        {"feature_name": "user_preferred_provider", "entity": "user_id", "data_type": "STRING", "freshness_sla_sec": 60, "description": "Most frequently selected inference engine"}
    ]
    df_features = pd.DataFrame(features_catalog)
    df_features["synced_at"] = datetime.now(timezone.utc).isoformat()

    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS neurolake_raw;")
    con.execute("CREATE OR REPLACE TABLE neurolake_raw.models AS SELECT * FROM df_models;")
    con.execute("CREATE OR REPLACE TABLE neurolake_raw.features_catalog AS SELECT * FROM df_features;")
    con.close()

    print(f"[dltHub] Ingested {len(df_models)} models and {len(df_features)} feature definitions.")

if __name__ == "__main__":
    run_dlt_metadata_ingestion()
