
SELECT 
    inference_id,
    cast(request_timestamp as TIMESTAMP) as request_timestamp,
    user_id,
    session_id,
    model_id,
    cast(prompt_tokens as INTEGER) as prompt_tokens,
    cast(completion_tokens as INTEGER) as completion_tokens,
    cast(total_tokens as INTEGER) as total_tokens,
    cast(latency_ms as INTEGER) as latency_ms,
    cast(vector_similarity_score as FLOAT) as vector_similarity_score,
    cast(cost_usd as DECIMAL(10,5)) as cost_usd,
    status,
    cache_hit
FROM neurolake_raw.ai_inference_events;
