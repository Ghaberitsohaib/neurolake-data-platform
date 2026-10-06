
SELECT 
    f.user_id,
    f.rolling_tokens_1h,
    f.avg_latency_ms,
    f.avg_vector_similarity,
    f.preferred_model,
    f.recent_request_count,
    f.last_updated_at
FROM neurolake_analytics.stg_features f;
