
SELECT 
    entity_id as user_id,
    feature_set,
    rolling_tokens_1h,
    avg_latency_ms,
    avg_vector_similarity,
    preferred_model,
    recent_request_count,
    cast(last_updated_at as TIMESTAMP) as last_updated_at
FROM neurolake_raw.online_features;
