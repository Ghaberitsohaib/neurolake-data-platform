import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import duckdb
import pytest

def test_pipeline_execution():
    from scripts.run_pipeline import run_entire_pipeline
    run_entire_pipeline()

    db_path = os.path.join(ROOT_DIR, "data_warehouse", "neurolake_warehouse.duckdb")
    assert os.path.exists(db_path), "Warehouse database does not exist!"

    con = duckdb.connect(db_path, read_only=False)
    
    # 1. Verify inference events
    inf_count = con.execute("SELECT count(*) FROM neurolake_analytics.fct_llm_inference_events").fetchone()[0]
    assert inf_count > 0, "No inference events in fact table!"

    # 2. Verify online feature store
    feat_count = con.execute("SELECT count(*) FROM neurolake_analytics.fct_user_feature_store").fetchone()[0]
    assert feat_count > 0, "No feature records in feature store!"

    # 3. Verify spark benchmarks
    bench_count = con.execute("SELECT count(*) FROM neurolake_analytics.spark_model_benchmarks").fetchone()[0]
    assert bench_count > 0, "No model benchmarks computed!"

    # 4. Verify data quality
    invalid_tokens = con.execute("SELECT count(*) FROM neurolake_analytics.fct_llm_inference_events WHERE total_tokens <= 0").fetchone()[0]
    assert invalid_tokens == 0, "Found invalid negative token counts!"

    con.close()
    print("All pytest assertions passed successfully!")

if __name__ == "__main__":
    test_pipeline_execution()
