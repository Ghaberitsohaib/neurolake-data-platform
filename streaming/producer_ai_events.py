"""
Kafka AI Telemetry & LLM Inference Stream Producer
Simulates high-velocity LLM interactions, token usage, and RAG vector search metrics.
"""
import uuid
import random
import time
from datetime import datetime, timezone

MODELS = [
    ("gpt-4o", 0.005, 0.015),
    ("claude-3-5-sonnet", 0.003, 0.015),
    ("llama-3-70b-instruct", 0.0009, 0.0009),
    ("mistral-large-2", 0.002, 0.006)
]

USERS = [f"USR_{i:04d}" for i in range(1, 35)]
STATUS_OPTIONS = ["SUCCESS", "SUCCESS", "SUCCESS", "SUCCESS", "RATE_LIMITED", "FALLBACK_TRIGGERED"]

def generate_ai_inference_event():
    model_id, prompt_rate, comp_rate = random.choice(MODELS)
    user_id = random.choice(USERS)
    prompt_tokens = random.randint(120, 2400)
    completion_tokens = random.randint(45, 1200)
    total_tokens = prompt_tokens + completion_tokens
    
    # Latency influenced by tokens & model
    base_latency = 350 if "llama" in model_id else (550 if "sonnet" in model_id else 750)
    latency_ms = int(base_latency + (completion_tokens * 0.8) + random.uniform(-60, 180))
    
    # RAG Vector similarity score (0.40 to 0.98)
    vector_similarity = round(random.betavariate(5, 2), 4)
    if vector_similarity > 0.99:
        vector_similarity = 0.985
    
    # Cost calculation
    cost_usd = round(((prompt_tokens / 1000.0) * prompt_rate) + ((completion_tokens / 1000.0) * comp_rate), 5)
    status = random.choice(STATUS_OPTIONS)

    now = datetime.now(timezone.utc)
    
    return {
        "inference_id": f"INF_{uuid.uuid4().hex[:12].upper()}",
        "request_timestamp": now.isoformat(),
        "user_id": user_id,
        "session_id": f"SES_{random.randint(100, 999)}",
        "model_id": model_id,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "latency_ms": max(latency_ms, 85),
        "vector_similarity_score": vector_similarity,
        "cost_usd": cost_usd,
        "status": status,
        "cache_hit": random.choice([True, False, False, False])
    }

def produce_stream(count=50):
    events = [generate_ai_inference_event() for _ in range(count)]
    return events

if __name__ == "__main__":
    sample = produce_stream(5)
    print("Generated sample event:", sample[0])
