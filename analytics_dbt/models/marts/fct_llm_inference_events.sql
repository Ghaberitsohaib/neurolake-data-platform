
SELECT 
    i.inference_id,
    i.request_timestamp,
    i.user_id,
    i.session_id,
    i.model_id,
    m.provider as model_provider,
    m.category as model_category,
    i.prompt_tokens,
    i.completion_tokens,
    i.total_tokens,
    i.latency_ms,
    i.vector_similarity_score,
    i.cost_usd,
    i.status,
    i.cache_hit
FROM neurolake_analytics.stg_llm_inference i
LEFT JOIN neurolake_analytics.stg_models m ON i.model_id = m.model_id;
