
SELECT inference_id, total_tokens 
FROM neurolake_analytics.fct_llm_inference_events 
WHERE total_tokens <= 0;
