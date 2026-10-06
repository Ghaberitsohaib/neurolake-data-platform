# NeuroLake — Real-Time ML Feature Store & GenAI Observability Lakehouse

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-Inference_Streaming-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![Spark](https://img.shields.io/badge/Apache_Spark-Model_Benchmarks-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![dbt](https://img.shields.io/badge/dbt-Dimensional_Marts-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Kestra](https://img.shields.io/badge/Kestra-Orchestration-8B5CF6?style=for-the-badge)](https://kestra.io/)
[![CI](https://github.com/Ghaberitsohaib/neurolake-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Ghaberitsohaib/neurolake-data-platform/actions/workflows/ci.yml)

> **NeuroLake** is an enterprise-scale, production-ready Data Engineering platform specifically designed for **Generative AI & Machine Learning Operations (LLMOps)**. It provides real-time online feature extraction for low-latency (<15ms) model inference, captures distributed LLM telemetry, computes token costs and P90/P99 latency percentiles with Apache Spark, and audits RAG vector retrieval similarity across multiple foundation models.

---

## Architecture Diagram

```mermaid
flowchart LR
    subgraph S1["1. Foundation Model Registry & Ingestion"]
        Registry["Model Registry & Feature Catalog"]
        DLT["dltHub Sync Engine"]
        Registry --> DLT
    end

    subgraph S2["2. Real-Time Streaming & Online Feature Store"]
        App["AI Applications & LLM Clients"]
        Kafka{{"Apache Kafka
(KRaft Mode)"}}
        FeatStore["Online Feature Store
(Sub-15ms Serving Layer)"]
        LakeSink["Bronze Lakehouse Sink
(Partitioned Parquet)"]
        App --> Kafka
        Kafka --> FeatStore
        Kafka --> LakeSink
    end

    subgraph S3["3. Multi-Tier Lakehouse Storage"]
        Bronze[("Bronze Layer
(Raw Parquet)")]
        Silver[("Silver Layer
(Typed Telemetry)")]
        Gold[("Gold Layer
(Model Benchmarks)")]
        Bronze --> Silver --> Gold
    end

    subgraph S4["4. Distributed Batch & Dimensional Modeling"]
        Spark["Apache Spark (PySpark)
(P50/P90/P99 Latency & Offline Features)"]
        DBT["dbt (Data Build Tool)
(Star Schema & Assertions)"]
        Warehouse[("Analytical Warehouse
(DuckDB / GCP BigQuery)")]
    end

    subgraph S5["5. Executive Command Console"]
        Console["Streamlit Executive UI
(Model Observability & Feature Inspector)"]
    end

    LakeSink --> Bronze
    DLT --> Warehouse
    Bronze --> Spark --> Gold
    Gold --> Warehouse
    Warehouse <--> DBT
    Warehouse --> Console
    FeatStore --> Console
```

---

## Key AI Data Engineering Concepts Implemented

| Domain Concept | Implementation in NeuroLake |
| :--- | :--- |
| **Real-Time Feature Store** | Ingests streaming inference events and computes rolling prompt token velocity, model affinity, and average retrieval relevance with sub-15ms lookup latency. |
| **LLM Cost & Token Observability** | Computes precise dollar burn rates across foundation models (GPT-4o, Claude 3.5 Sonnet, Llama 3 70B, Mistral Large 2) per 1,000 tokens. |
| **RAG Vector Search Telemetry** | Tracks Cosine similarity scores between prompt embeddings and knowledge base chunks, detecting retrieval drift and correlation with response latency. |
| **Distributed Percentile Benchmarking** | PySpark batch job calculating median (P50), tail (P90), and worst-case (P99) response latencies across thousands of distributed requests. |
| **Data Quality Assertions** | Automated **dbt tests** verifying non-negative token volumes, entity primary keys, and model referential integrity. |
| **Infrastructure as Code (IaC)** | Modular **Terraform** configurations provisioning GCP Cloud Storage buckets and partitioned BigQuery datasets. |

---

## Repository Structure

```
neurolake-data-platform/
├── docker-compose.yml              # Cluster: Kafka, MinIO, Spark, Kestra, Dashboard
├── requirements.txt                # Python libraries
├── terraform/                      # Terraform GCP BigQuery & GCS Buckets
├── ingestion/                      # dltHub pipelines for Model Registry & Feature Catalog
├── streaming/                      # Kafka AI event producer, online feature extractor, lakehouse sink
├── batch/                          # PySpark model benchmarking & offline training snapshots
├── analytics_dbt/                  # dbt models (stg_*, fct_*) & automated tests
├── orchestration/flows/            # Kestra declarative workflow DAGs
├── data_platform/                  # Streamlit Executive GenAI & Feature Store UI
├── scripts/                        # Automated pipeline execution scripts
└── tests/                          # Automated pytest suite
```

---

## Quickstart: Running in 30 Seconds

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Execute the entire pipeline locally:
```bash
python scripts/run_pipeline.py
```

### 3. Launch the Executive AI & Feature Store Dashboard:
```bash
streamlit run data_platform/dashboard.py
```
Open **`http://localhost:8501`** to view real-time foundation model benchmarks, query online entity features, and inspect token consumption analytics.

---

## Full Docker Multi-Container Cluster

```bash
docker compose up -d
```
- **Streamlit Command Console**: `http://localhost:8502`
- **Kafka Stream Monitor**: `http://localhost:9092`
- **MinIO Lakehouse Console**: `http://localhost:9001`
