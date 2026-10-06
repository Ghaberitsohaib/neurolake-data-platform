import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
import time
from ingestion.dlt_models_metadata_pipeline import run_dlt_metadata_ingestion
from streaming.consumer_to_lakehouse import sink_stream_to_lakehouse
from batch.spark_feature_aggregation_job import run_spark_feature_batch
from analytics_dbt.run_dbt import run_dbt_models

def run_entire_pipeline():
    start_time = time.time()
    print("=================================================================")
    print("  [START] NeuroLake: Executing End-to-End AI Lakehouse Pipeline")
    print("=================================================================")

    # 1. dltHub Ingestion
    run_dlt_metadata_ingestion()

    # 2. Kafka Streaming & Online Feature Extraction
    sink_stream_to_lakehouse(120)

    # 3. Apache Spark Batch Benchmarking
    run_spark_feature_batch()

    # 4. dbt Dimensional Models & Quality Assertions
    run_dbt_models()

    elapsed = round(time.time() - start_time, 2)
    print("=================================================================")
    print(f"  [SUCCESS] NeuroLake Pipeline Completed Successfully in {elapsed}s!")
    print("=================================================================")

if __name__ == "__main__":
    run_entire_pipeline()
