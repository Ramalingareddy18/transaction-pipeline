import os
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from anomaly_detection import detect_anomalies

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Page Configuration
st.set_page_config(
    page_title="Transaction Intelligence & Anomaly Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #0b0f19;
        background-image: 
            radial-gradient(at 10% 10%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
            radial-gradient(at 90% 80%, rgba(168, 85, 247, 0.10) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
    }

    /* Custom Header Banner */
    .portal-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .portal-title {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .portal-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    /* Glassmorphic Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(22, 31, 48, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1rem 1.25rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: rgba(99, 102, 241, 0.4);
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }

    /* Custom Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.9rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Custom Header Banner
st.markdown("""
<div class="portal-header">
    <div>
        <h1 class="portal-title">⚡ Transaction Intelligence & ML Portal</h1>
        <p class="portal-subtitle">Enterprise Real-Time Analytics & Machine Learning Isolation Forest Anomaly Detection</p>
    </div>
    <div>
        <span class="status-badge">🟢 System Online & ML Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

transactions = None
fetch_error = None
data_source = None

# Attempt 1: Fetch from FastAPI API Server
try:
    response = requests.get(f"{API_BASE_URL}/transactions?limit=1000", timeout=5)
    response.raise_for_status()
    transactions = response.json()
    data_source = "FastAPI API Backend"
except Exception as exc:
    fetch_error = str(exc)

# Attempt 2: Direct Database Fallback if API is offline
if transactions is None:
    try:
        from app.database import SessionLocal, Transaction
        from sqlalchemy import select
        with SessionLocal() as session:
            rows = session.execute(select(Transaction)).scalars().all()
            transactions = [
                {
                    "transaction_id": row.transaction_id,
                    "date": row.date.isoformat() if row.date else None,
                    "description": row.description,
                    "amount": row.amount,
                    "currency": row.currency,
                    "category": row.category,
                    "account": row.account,
                    "transaction_type": row.transaction_type,
                    "month": row.month,
                    "year": row.year,
                }
                for row in rows
            ]
        if transactions:
            data_source = "PostgreSQL Direct"
            st.info("ℹ️ Connected directly to PostgreSQL database.")
    except Exception as db_exc:
        fetch_error += f" | Direct DB Fallback: {db_exc}"

if transactions is None:
    st.error(f"❌ Unable to load transactions data.")
    st.warning("Please ensure PostgreSQL database is running or launch the backend API.")
    if st.button("🔄 Retry Connection"):
        st.rerun()
    st.stop()

if not transactions:
    st.warning("⚠️ No transactions found in the database. Run the ETL pipeline to load data:")
    st.code("python src/etl_pipeline.py")
    if st.button("🔄 Refresh Data"):
        st.rerun()
    st.stop()

frame = pd.DataFrame(transactions)
if "date" in frame.columns:
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
if "amount" in frame.columns:
    frame["amount"] = pd.to_numeric(frame["amount"], errors="coerce")

# Real Machine Learning Anomaly Detection via Isolation Forest
df_anomalies = detect_anomalies(frame)
anomaly_count = int(df_anomalies["is_anomaly"].sum())

# Sidebar Controls & Information
st.sidebar.markdown("### 🎛️ Portal Controls")
show_only_anomalies = st.sidebar.checkbox("🚨 Show Only Flagged Anomalies", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 ML Model Specs")
st.sidebar.markdown("- **Algorithm**: `IsolationForest`")
st.sidebar.markdown("- **Contamination Rate**: `10%`")
st.sidebar.markdown(f"- **Flagged Outliers**: `{anomaly_count}`")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌐 Enterprise Web Portal")
st.sidebar.markdown("[Open Full Portal UI](http://127.0.0.1:8000/dashboard)")

# Top KPI Summary Cards
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("TOTAL VOLUME", f"${frame['amount'].sum():,.2f}")
col2.metric("TRANSACTIONS", f"{len(frame):,}")
col3.metric("AVERAGE AMOUNT", f"${frame['amount'].mean():,.2f}")
col4.metric("🚨 ML ANOMALIES", f"{anomaly_count} ({anomaly_count / len(frame) * 100:.1f}%)")
col5.metric("DATA SOURCE", data_source)

st.markdown("<br>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_analytics, tab_ml, tab_explorer = st.tabs(["📊 Analytics Overview", "🤖 ML Anomaly Detection", "🔍 Transactions Explorer"])

with tab_analytics:
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 💰 Spending Breakdown by Category")
        if "category" in frame.columns:
            category_totals = frame.groupby("category", dropna=False)["amount"].sum().reset_index()
            fig_bar = px.bar(
                category_totals,
                x="category",
                y="amount",
                labels={"category": "Category", "amount": "Total ($)"},
                color="category",
                template="plotly_dark",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.markdown("#### 📈 Daily Cashflow Trend")
        if "date" in frame.columns and frame["date"].notna().any():
            daily = frame.groupby(frame["date"].dt.date)["amount"].sum().reset_index()
            daily.columns = ["date", "amount"]
            fig_line = px.area(
                daily,
                x="date",
                y="amount",
                labels={"date": "Date", "amount": "Amount ($)"},
                template="plotly_dark",
                markers=True
            )
            fig_line.update_traces(line_color="#6366f1", fillcolor="rgba(99, 102, 241, 0.2)")
            fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_line, use_container_width=True)

with tab_ml:
    st.markdown("#### 🚨 Machine Learning Outlier Detection (Isolation Forest)")
    st.info("The Isolation Forest algorithm isolates anomalous transactions by randomly selecting a feature and splitting values.")

    col_m1, col_m2 = st.columns([1, 2])

    with col_m1:
        st.error(f"⚠️ **{anomaly_count} Outliers Flagged** out of {len(frame)} records.")
        flagged_df = df_anomalies[df_anomalies["is_anomaly"]]
        if not flagged_df.empty:
            st.markdown("##### High Severity Transactions:")
            for idx, row in flagged_df.iterrows():
                st.markdown(
                    f"🔴 **#{row['transaction_id']}** — `${row['amount']:,.2f}`  \n"
                    f"*Desc*: {row.get('description', 'N/A')}  \n"
                    f"*Category*: `{row.get('category', 'N/A')}` | Score: `{row.get('anomaly_score', 0):.3f}`"
                )
                st.markdown("---")

    with col_m2:
        st.markdown("##### Isolation Forest Scatter Map (Red = Anomaly)")
        fig_scatter = px.scatter(
            df_anomalies,
            x="transaction_id",
            y="amount",
            color="is_anomaly",
            color_discrete_map={True: "#ef4444", False: "#3b82f6"},
            hover_data=["description", "category", "anomaly_score"],
            template="plotly_dark",
            title="Transaction Amount Distribution & ML Classification"
        )
        fig_scatter.update_traces(marker=dict(size=12, opacity=0.85))
        fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab_explorer:
    st.markdown("#### 🔍 Real-Time Transactions Grid")
    display_df = df_anomalies[df_anomalies["is_anomaly"]] if show_only_anomalies else df_anomalies
    cols_to_show = [
        c for c in ["transaction_id", "date", "description", "amount", "currency", "category", "account", "is_anomaly", "anomaly_score"]
        if c in display_df.columns
    ]
    st.dataframe(display_df[cols_to_show], use_container_width=True)
