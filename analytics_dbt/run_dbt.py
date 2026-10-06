"""
dbt Transformation & Data Quality Test Engine targeting DuckDB.
"""
import os
import duckdb

def run_dbt_models():
    print("[dbt Engine] Compiling & executing staging and marts transformations...")
    db_path = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "neurolake_warehouse.duckdb")
    con = duckdb.connect(db_path, read_only=False)
    con.execute("CREATE SCHEMA IF NOT EXISTS neurolake_analytics;")

    # 1. Staging Views
    con.execute("""
        CREATE OR REPLACE VIEW neurolake_analytics.stg_llm_inference AS
        SELECT 
            inference_id,
            cast(request_timestamp as TIMESTAMP) as request_timestamp,
            user_id, session_id, model_id,
            cast(prompt_tokens as INTEGER) as prompt_tokens,
            cast(completion_tokens as INTEGER) as completion_tokens,
            cast(total_tokens as INTEGER) as total_tokens,
            cast(latency_ms as INTEGER) as latency_ms,
            cast(vector_similarity_score as FLOAT) as vector_similarity_score,
            cast(cost_usd as DECIMAL(10,5)) as cost_usd,
            status, cache_hit
        FROM neurolake_raw.ai_inference_events;
    """)

    con.execute("""
        CREATE OR REPLACE VIEW neurolake_analytics.stg_models AS
        SELECT 
            model_id, provider, category, context_window,
            prompt_cost_per_1k, completion_cost_per_1k, is_active
        FROM neurolake_raw.models;
    """)

    con.execute("""
        CREATE OR REPLACE VIEW neurolake_analytics.stg_features AS
        SELECT 
            entity_id as user_id, feature_set, rolling_tokens_1h,
            avg_latency_ms, avg_vector_similarity, preferred_model,
            recent_request_count, cast(last_updated_at as TIMESTAMP) as last_updated_at
        FROM neurolake_raw.online_features;
    """)

    # 2. Dimensional Fact Marts
    con.execute("""
        CREATE OR REPLACE TABLE neurolake_analytics.fct_llm_inference_events AS
        SELECT 
            i.inference_id, i.request_timestamp, i.user_id, i.session_id, i.model_id,
            coalesce(m.provider, 'Unknown') as model_provider,
            coalesce(m.category, 'LLM') as model_category,
            i.prompt_tokens, i.completion_tokens, i.total_tokens,
            i.latency_ms, i.vector_similarity_score, i.cost_usd,
            i.status, i.cache_hit
        FROM neurolake_analytics.stg_llm_inference i
        LEFT JOIN neurolake_analytics.stg_models m ON i.model_id = m.model_id;
    """)

    con.execute("""
        CREATE OR REPLACE TABLE neurolake_analytics.fct_user_feature_store AS
        SELECT 
            user_id, rolling_tokens_1h, avg_latency_ms,
            avg_vector_similarity, preferred_model, recent_request_count, last_updated_at
        FROM neurolake_analytics.stg_features;
    """)

    # 3. Data Quality Assertions
    invalid_tokens = con.execute("SELECT count(*) FROM neurolake_analytics.fct_llm_inference_events WHERE total_tokens <= 0").fetchone()[0]
    assert invalid_tokens == 0, f"dbt Test Failed: {invalid_tokens} records with non-positive total_tokens!"

    con.close()
    print("[dbt Engine] Models compiled, marts populated, and quality assertions passed!")

if __name__ == "__main__":
    run_dbt_models()
