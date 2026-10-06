import sys, os
from pathlib import Path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import duckdb
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="NeuroLake | Real-Time ML Feature Store & GenAI Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# HIGH-END CORPORATE AI DESIGN SYSTEM (CSS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background-color: #070b14 !important;
    background-image: radial-gradient(circle at 10% 10%, #0d1527 0%, #060911 60%, #04060a 100%) !important;
    color: #f8fafc !important;
}

section[data-testid="stSidebar"] {
    background-color: #0c1322 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
    padding-top: 1.5rem !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p {
    color: #f1f5f9 !important;
}

section[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #141e33 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #f8fafc !important;
    font-weight: 500 !important;
}

div[data-baseweb="popover"] ul {
    background-color: #141e33 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
}

div[data-baseweb="popover"] li {
    color: #f8fafc !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: #1e293b !important;
}

/* Action Buttons */
button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

button[kind="secondary"] {
    background: #141e33 !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 16px !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover {
    background: #1e293b !important;
    border-color: rgba(99, 102, 241, 0.5) !important;
    color: #ffffff !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background-color: #0c1322 !important;
    padding: 6px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px !important;
    padding: 8px 16px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #cbd5e1 !important;
    border: none !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35) !important;
}

/* Banner */
.top-banner {
    background: linear-gradient(135deg, rgba(23, 33, 56, 0.9) 0%, rgba(11, 17, 30, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(16px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.banner-title {
    font-size: 1.85rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 40%, #cbd5e1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.banner-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 5px;
    font-weight: 400;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* Metric Cards */
.kpi-card {
    background: linear-gradient(145deg, rgba(23, 33, 56, 0.85) 0%, rgba(13, 19, 34, 0.98) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, border-color 0.2s ease;
    margin-bottom: 12px;
}

.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99, 102, 241, 0.4);
}

.kpi-card-emerald { border-top: 3px solid #10b981; }
.kpi-card-indigo  { border-top: 3px solid #6366f1; }
.kpi-card-amber   { border-top: 3px solid #f59e0b; }
.kpi-card-cyan    { border-top: 3px solid #06b6d4; }
.kpi-card-rose    { border-top: 3px solid #f43f5e; }

.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.kpi-title {
    color: #94a3b8;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    white-space: nowrap;
}

.kpi-pill {
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 4px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.kpi-pill-emerald { background: rgba(16, 185, 129, 0.18); color: #34d399; }
.kpi-pill-indigo  { background: rgba(99, 102, 241, 0.18); color: #a5b4fc; }
.kpi-pill-amber   { background: rgba(245, 158, 11, 0.18); color: #fcd34d; }
.kpi-pill-cyan    { background: rgba(6, 182, 212, 0.18); color: #67e8f9; }
.kpi-pill-rose    { background: rgba(244, 63, 94, 0.18); color: #fda4af; }

.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #f8fafc;
    line-height: 1.2;
    font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
}

.kpi-value-emerald { color: #34d399; }
.kpi-value-indigo  { color: #a5b4fc; }
.kpi-value-amber   { color: #fcd34d; }
.kpi-value-cyan    { color: #67e8f9; }
.kpi-value-rose    { color: #fda4af; }

.kpi-footer {
    margin-top: 7px;
    font-size: 0.74rem;
    color: #94a3b8;
    display: flex;
    align-items: center;
    gap: 6px;
}

.kpi-tag-success { color: #34d399; font-weight: 600; }
.kpi-tag-danger  { color: #fb7185; font-weight: 600; }

.glass-panel {
    background: linear-gradient(145deg, rgba(20, 28, 48, 0.75) 0%, rgba(11, 16, 28, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    backdrop-filter: blur(12px);
    margin-bottom: 18px;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATABASE DATA ACCESS (Zero Locking)
# -----------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data_warehouse", "neurolake_warehouse.duckdb")

def load_warehouse_data():
    if not os.path.exists(DB_PATH):
        return None, None, None
    con = duckdb.connect(DB_PATH, read_only=False)
    try:
        inf_df = con.execute("SELECT * FROM neurolake_analytics.fct_llm_inference_events;").df()
        bench_df = con.execute("SELECT * FROM neurolake_analytics.spark_model_benchmarks;").df()
        feat_df = con.execute("SELECT * FROM neurolake_analytics.fct_user_feature_store;").df()
        return inf_df, bench_df, feat_df
    finally:
        con.close()

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 6px 0 16px 0;">
    <h2 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0;">
        Pipeline Console
    </h2>
    <p style="color: #94a3b8; font-size: 0.78rem; margin: 4px 0 0 0;">AI feature store & streaming telemetry</p>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Emit AI Inference Stream (60 Events)", use_container_width=True, type="primary"):
    with st.spinner("Emitting LLM inference events & extracting online features..."):
        from streaming.consumer_to_lakehouse import sink_stream_to_lakehouse
        sink_stream_to_lakehouse(60)
        from analytics_dbt.run_dbt import run_dbt_models
        run_dbt_models()
        from batch.spark_feature_aggregation_job import run_spark_feature_batch
        run_spark_feature_batch()
    st.sidebar.success("60 inference events streamed & feature store synced.")
    st.rerun()

if st.sidebar.button("Run Spark Benchmarks", use_container_width=True):
    with st.spinner("Executing PySpark model benchmarking & P90 latency aggregates..."):
        from batch.spark_feature_aggregation_job import run_spark_feature_batch
        run_spark_feature_batch()
    st.sidebar.success("Spark offline aggregation finished.")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='font-size: 0.85rem; font-weight: 700; color: #94a3b8; text-transform: uppercase;'>Telemetry Filters</h3>", unsafe_allow_html=True)

# Check DB exists
if not os.path.exists(DB_PATH):
    st.warning("Warehouse database not initialized.")
    if st.button("Initialize NeuroLake Pipeline", type="primary"):
        with st.spinner("Executing end-to-end pipeline initialization..."):
            from scripts.run_pipeline import run_entire_pipeline
            run_entire_pipeline()
        st.rerun()
    st.stop()

inf_df, bench_df, feat_df = load_warehouse_data()
if inf_df is None or len(inf_df) == 0:
    st.info("No inference telemetry found. Run the pipeline to initialize data.")
    st.stop()

# Interactive Filters
selected_model = st.sidebar.selectbox("Foundation Model", ["ALL"] + sorted(inf_df['model_id'].unique().tolist()))
selected_status = st.sidebar.selectbox("Inference Status", ["ALL", "SUCCESS", "RATE_LIMITED", "FALLBACK_TRIGGERED"])
filter_cache = st.sidebar.selectbox("Cache Hits", ["ALL", "CACHE_HIT", "CACHE_MISS"])

# Filter data
filtered_inf = inf_df.copy()
if selected_model != "ALL":
    filtered_inf = filtered_inf[filtered_inf['model_id'] == selected_model]
if selected_status != "ALL":
    filtered_inf = filtered_inf[filtered_inf['status'] == selected_status]
if filter_cache == "CACHE_HIT":
    filtered_inf = filtered_inf[filtered_inf['cache_hit'] == True]
elif filter_cache == "CACHE_MISS":
    filtered_inf = filtered_inf[filtered_inf['cache_hit'] == False]

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="background: rgba(20, 30, 50, 0.7); padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.08);">
    <div style="color: #94a3b8; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Infrastructure Status</div>
    <div style="margin-top: 8px; font-size: 0.8rem; display: flex; flex-direction: column; gap: 6px;">
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Kafka:</b> <span style="color:#94a3b8;">Inference Stream</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Feature Store:</b> <span style="color:#94a3b8;">Sub-15ms Serving</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Lakehouse:</b> <span style="color:#94a3b8;">MinIO Parquet</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Batch:</b> <span style="color:#94a3b8;">PySpark Model Metrics</span></div>
        <div><span style="color:#10b981; font-weight:bold;">●</span> <b style="color:#f8fafc;">Engine:</b> <span style="color:#94a3b8;">DuckDB / BigQuery</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TOP HERO BANNER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="top-banner">
    <div>
        <h1 class="banner-title">NeuroLake Command Center</h1>
        <p class="banner-subtitle">
            Enterprise Real-Time ML Feature Store • LLM Telemetry & Cost Observability • Vector Retrieval Lakehouse
        </p>
    </div>
    <div style="display: flex; gap: 10px; align-items: center;">
        <div class="status-pill">
            <span class="pulse-dot"></span>
            INFERENCE STREAM ACTIVE
        </div>
        <div style="background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); color: #a5b4fc; padding: 5px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700;">
            FEATURE SLA: < 15MS
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# EXECUTIVE KPI METRICS
# -----------------------------------------------------------------------------
total_inferences = len(filtered_inf)
total_tokens = int(filtered_inf['total_tokens'].sum())
total_cost = float(filtered_inf['cost_usd'].sum())
avg_latency = float(filtered_inf['latency_ms'].mean()) if total_inferences > 0 else 0
avg_similarity = float(filtered_inf['vector_similarity_score'].mean()) if total_inferences > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
<div class="kpi-card kpi-card-emerald">
    <div class="kpi-header">
        <span class="kpi-title">Inference Requests</span>
        <span class="kpi-pill kpi-pill-emerald">REQS</span>
    </div>
    <div class="kpi-value kpi-value-emerald">{total_inferences:,}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">Active Stream</span>
        <span>Across foundation models</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
<div class="kpi-card kpi-card-indigo">
    <div class="kpi-header">
        <span class="kpi-title">Total Tokens Burned</span>
        <span class="kpi-pill kpi-pill-indigo">TOKENS</span>
    </div>
    <div class="kpi-value kpi-value-indigo">{total_tokens:,}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">Prompt + Comp</span>
        <span>Avg {(total_tokens / total_inferences if total_inferences > 0 else 0):.0f} / req</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
<div class="kpi-card kpi-card-amber">
    <div class="kpi-header">
        <span class="kpi-title">Inference Cost</span>
        <span class="kpi-pill kpi-pill-amber">USD</span>
    </div>
    <div class="kpi-value kpi-value-amber">${total_cost:.4f}</div>
    <div class="kpi-footer">
        <span style="color: #fbbf24; font-weight: 600;">Avg ${(total_cost * 1000 / total_tokens if total_tokens > 0 else 0):.4f}</span>
        <span>Per 1K tokens</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
<div class="kpi-card kpi-card-cyan">
    <div class="kpi-header">
        <span class="kpi-title">Avg Latency</span>
        <span class="kpi-pill kpi-pill-cyan">SPEED</span>
    </div>
    <div class="kpi-value kpi-value-cyan">{avg_latency:.0f} <span style="font-size: 0.9rem; color: #94a3b8;">ms</span></div>
    <div class="kpi-footer">
        <span style="color: #22d3ee; font-weight: 600;">Sub-Second</span>
        <span>Time-to-first-token included</span>
    </div>
</div>
""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
<div class="kpi-card kpi-card-rose">
    <div class="kpi-header">
        <span class="kpi-title">RAG Vector Match</span>
        <span class="kpi-pill kpi-pill-rose">COSINE</span>
    </div>
    <div class="kpi-value kpi-value-rose">{avg_similarity:.3f}</div>
    <div class="kpi-footer">
        <span class="kpi-tag-success">High Quality</span>
        <span>Knowledge retrieval relevance</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Plotly theme layout helper
def get_dark_plotly_layout(height=340):
    return dict(
        height=height,
        margin=dict(l=15, r=15, t=35, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color="#94a3b8", size=12),
        hoverlabel=dict(bgcolor="#1e293b", font_color="#f8fafc", font_size=12)
    )

# -----------------------------------------------------------------------------
# TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Foundation Model Observability",
    "Real-Time Feature Store",
    "RAG Vector Search Analytics",
    "Atomic Inference Stream",
    "AI Platform Architecture"
])

# TAB 1: MODEL BENCHMARKS
with tab1:
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Token Usage Distribution by Model
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Distribution of compute tokens across foundation model providers</p>
</div>
""", unsafe_allow_html=True)
        model_df = filtered_inf.groupby("model_id")['total_tokens'].sum().reset_index()
        fig_tokens = px.pie(
            model_df,
            names="model_id",
            values="total_tokens",
            hole=0.55,
            color="model_id",
            color_discrete_map={
                "gpt-4o": "#10b981",
                "claude-3-5-sonnet": "#6366f1",
                "llama-3-70b-instruct": "#f59e0b",
                "mistral-large-2": "#ec4899"
            }
        )
        fig_tokens.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='#0b0f19', width=2))
        )
        fig_tokens.update_layout(**get_dark_plotly_layout(height=310))
        st.plotly_chart(fig_tokens, use_container_width=True)

    with c_right:
        st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Model Latency Comparison (P50 vs P90 vs P99)
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Response time profiles computed by Apache Spark batch job</p>
</div>
""", unsafe_allow_html=True)
        if len(bench_df) > 0:
            fig_lat = go.Figure()
            fig_lat.add_trace(go.Bar(name='P50 Median', x=bench_df['model_id'], y=bench_df['p50_latency_ms'], marker_color='#10b981'))
            fig_lat.add_trace(go.Bar(name='P90 Tail', x=bench_df['model_id'], y=bench_df['p90_latency_ms'], marker_color='#6366f1'))
            fig_lat.add_trace(go.Bar(name='P99 Worst', x=bench_df['model_id'], y=bench_df['p99_latency_ms'], marker_color='#f43f5e'))
            fig_lat.update_layout(
                barmode='group',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Milliseconds"),
                **get_dark_plotly_layout(height=310)
            )
            st.plotly_chart(fig_lat, use_container_width=True)

    # Cost breakdown table
    st.markdown("<h4 style='font-size: 0.95rem; font-weight: 700; color: #f8fafc; margin-top: 15px;'>Foundation Model Cost & Efficiency Summary (Spark Gold Mart)</h4>", unsafe_allow_html=True)
    if len(bench_df) > 0:
        st.dataframe(
            bench_df.style.format({
                'total_cost_usd': '${:,.4f}',
                'cost_per_1k_tokens': '${:,.5f}',
                'avg_latency_ms': '{:,.1f} ms',
                'total_tokens': '{:,}',
                'cache_hit_rate_pct': '{:.1f}%',
                'success_rate_pct': '{:.1f}%'
            }),
            use_container_width=True
        )

# TAB 2: FEATURE STORE
with tab2:
    st.markdown("""
<div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(15, 23, 42, 0.4) 100%); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; padding: 18px 22px; margin-bottom: 20px;">
    <h4 style="color: #a5b4fc; margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 700;">
        Online Feature Store: Low-Latency Serving Layer
    </h4>
    <p style="color: #cbd5e1; font-size: 0.85rem; margin: 0; line-height: 1.5;">
        Real-time feature values extracted continuously from incoming inference streams for sub-15ms live scoring, model routing, and prompt optimization.
    </p>
</div>
""", unsafe_allow_html=True)

    col_f_search, col_f_meta = st.columns([1, 2])
    with col_f_search:
        target_user = st.selectbox("Lookup User Entity ID", sorted(feat_df['user_id'].unique().tolist()) if len(feat_df) > 0 else ["USR_0001"])
    
    user_feature = feat_df[feat_df['user_id'] == target_user]
    if not user_feature.empty:
        u_row = user_feature.iloc[0]
        st.markdown(f"""
<div class="glass-panel" style="margin-top: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <h4 style="color: #f8fafc; margin: 0; font-size: 1.1rem;">Entity: <code>{u_row['user_id']}</code></h4>
        <span class="status-pill"><span class="pulse-dot"></span>ONLINE FEATURE SERVING READY</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px;">
        <div>
            <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Rolling Tokens (1h)</div>
            <div style="color: #34d399; font-size: 1.4rem; font-weight: 800; font-family: 'JetBrains Mono';">{u_row['rolling_tokens_1h']:,}</div>
        </div>
        <div>
            <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Average Latency</div>
            <div style="color: #a5b4fc; font-size: 1.4rem; font-weight: 800; font-family: 'JetBrains Mono';">{u_row['avg_latency_ms']:.1f} ms</div>
        </div>
        <div>
            <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Mean RAG Similarity</div>
            <div style="color: #67e8f9; font-size: 1.4rem; font-weight: 800; font-family: 'JetBrains Mono';">{u_row['avg_vector_similarity']:.4f}</div>
        </div>
        <div>
            <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; text-transform: uppercase;">Preferred Model</div>
            <div style="color: #fcd34d; font-size: 1.1rem; font-weight: 800;">{u_row['preferred_model']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<h4 style='font-size: 0.95rem; font-weight: 700; color: #f8fafc; margin-top: 15px;'>Active Entity Features Table (dbt Star Schema)</h4>", unsafe_allow_html=True)
    st.dataframe(
        feat_df.style.format({
            'rolling_tokens_1h': '{:,}',
            'avg_latency_ms': '{:.1f} ms',
            'avg_vector_similarity': '{:.4f}'
        }),
        use_container_width=True
    )

# TAB 3: RAG VECTOR SEARCH
with tab3:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        RAG Vector Search Relevance & Retrieval Latency
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Correlation between embedding Cosine similarity score and response latency</p>
</div>
""", unsafe_allow_html=True)

    col_r1, col_r2 = st.columns([1, 1])
    with col_r1:
        fig_scatter = px.scatter(
            filtered_inf,
            x="vector_similarity_score",
            y="latency_ms",
            color="model_id",
            size="total_tokens",
            hover_data=["inference_id", "user_id", "cost_usd"],
            color_discrete_sequence=["#10b981", "#6366f1", "#f59e0b", "#ec4899"]
        )
        fig_scatter.update_layout(
            xaxis=dict(title="Cosine Similarity Score", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Latency (ms)", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            **get_dark_plotly_layout(height=340)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_r2:
        fig_hist = px.histogram(
            filtered_inf,
            x="vector_similarity_score",
            nbins=15,
            color_discrete_sequence=["#6366f1"]
        )
        fig_hist.update_layout(
            xaxis=dict(title="Cosine Similarity Range", showgrid=False),
            yaxis=dict(title="Frequency", showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
            **get_dark_plotly_layout(height=340)
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# TAB 4: ATOMIC INFERENCE STREAM
with tab4:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.05rem; font-weight: 700; color: #f8fafc; margin: 0 0 4px 0;">
        Raw Telemetry Stream & Token Cost Audit
    </h3>
    <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">Atomic inference events partitioned in Lakehouse (Parquet) and queried in DuckDB</p>
</div>
""", unsafe_allow_html=True)
    
    st.dataframe(
        filtered_inf.sort_values(by="request_timestamp", ascending=False).head(100)[[
            'inference_id', 'request_timestamp', 'user_id', 'model_id',
            'prompt_tokens', 'completion_tokens', 'total_tokens', 'latency_ms',
            'vector_similarity_score', 'cost_usd', 'status', 'cache_hit'
        ]].style.format({
            'prompt_tokens': '{:,}',
            'completion_tokens': '{:,}',
            'total_tokens': '{:,}',
            'latency_ms': '{:,} ms',
            'vector_similarity_score': '{:.4f}',
            'cost_usd': '${:,.5f}'
        }),
        use_container_width=True
    )

# TAB 5: ARCHITECTURE
with tab5:
    st.markdown("""
<div class="glass-panel">
    <h3 style="font-size: 1.15rem; font-weight: 800; color: #f8fafc; margin: 0 0 8px 0;">
        End-to-End GenAI Data Lakehouse Stack
    </h3>
    <p style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
        NeuroLake bridges production AI models with robust lakehouse pipelines, delivering real-time feature extraction for live inference and batch benchmarking for offline ML training.
    </p>
</div>
""", unsafe_allow_html=True)

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #6366f1; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">1. Ingestion & Streaming</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>Apache Kafka (KRaft)</b>: High-throughput ingestion of LLM inference telemetry.<br>
        • <b>dltHub Pipeline</b>: Syncs Model Registry and Feature Catalog definitions.<br>
        • <b>Online Feature Store</b>: Sliding window feature extraction (<15ms SLA).
    </p>
</div>
""", unsafe_allow_html=True)
    with col_a2:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #06b6d4; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">2. Multi-Tier Lakehouse</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>Bronze Layer</b>: Raw partitioned Parquet sinks in MinIO.<br>
        • <b>PySpark Distributed Engine</b>: Aggregates latency P50/P90/P99 percentiles.<br>
        • <b>Gold Ledger</b>: Model cost efficiency benchmarks and offline training snapshots.
    </p>
</div>
""", unsafe_allow_html=True)
    with col_a3:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px; height: 100%;">
    <div style="color: #10b981; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">3. Analytics & Orchestration</div>
    <p style="color: #94a3b8; font-size: 0.82rem; line-height: 1.5;">
        • <b>dbt (Data Build Tool)</b>: Dimensional star schema for AI cost observability.<br>
        • <b>Data Quality Tests</b>: Automated assertions on token volume integrity.<br>
        • <b>Kestra DAGs</b>: Declarative workflow orchestration.
    </p>
</div>
""", unsafe_allow_html=True)
