
SELECT 
    model_id,
    provider,
    category,
    context_window,
    prompt_cost_per_1k,
    completion_cost_per_1k,
    is_active
FROM neurolake_raw.models;
