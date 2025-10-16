import streamlit as st
import pandas as pd
import json, os
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Data Drift Watch",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- FILE PATHS ----------
META_PATH = os.path.join(os.path.dirname(__file__), '..', 'metadata', 'run_log.jsonl')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'metadata', 'air_quality.csv')

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .big-font {
        font-size:36px !important;
        font-weight:700;
        color:#2C3E50;
    }
    .metric-card {
        background-color:#F7F9FB;
        padding:20px;
        border-radius:12px;
        box-shadow:0 1px 3px rgba(0,0,0,0.1);
        text-align:center;
    }
    .footer {
        text-align:center;
        font-size:14px;
        margin-top:50px;
        color:#888;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<p class="big-font">Data Drift Watch</p>', unsafe_allow_html=True)
st.markdown("##### A live, interactive dashboard to monitor dataset drift, data quality, and health over time.")

# Auto-refresh every 60s
st_autorefresh(interval=60000, key="refresh")

# ---------- MAIN LOGIC ----------
if os.path.exists(META_PATH):
    logs = [json.loads(line) for line in open(META_PATH)]
    df_meta = pd.DataFrame(logs)
    drift_df = pd.DataFrame(df_meta['drift_scores'].to_list(), index=pd.to_datetime(df_meta['timestamp']))

    # ---------- SIDEBAR ----------
    st.sidebar.header("🔍 Filters & Controls")
    columns = st.sidebar.multiselect("Select Features", drift_df.columns.tolist(), default=drift_df.columns[:5].tolist())
    st.sidebar.write(f"Total Runs: **{len(df_meta)}**")
    avg_drift = round(drift_df[columns].mean().mean(), 4)
    st.sidebar.metric("📊 Avg Drift", avg_drift)

    if st.sidebar.button("🔄 Refresh Data"):
        os.system("python src/ingest.py && python src/drift_detector.py")
        st.experimental_rerun()

    # ---------- TOP METRICS ----------
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><h4>🧮 Total Runs</h4><h2>{}</h2></div>'.format(len(df_meta)), unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h4>📊 Avg Drift</h4><h2>{}</h2></div>'.format(avg_drift), unsafe_allow_html=True)
    with col3:
        max_drift = round(drift_df[columns].max().max(), 4)
        st.markdown('<div class="metric-card"><h4>🚦 Max Drift</h4><h2>{}</h2></div>'.format(max_drift), unsafe_allow_html=True)

    # ---------- TABS ----------
    tab1, tab2, tab3 = st.tabs(["📈 Drift Trends", "🧾 Run History", "💾 Latest Data"])

    # ----- TAB 1: Drift Chart -----
    with tab1:
        st.subheader("Feature Drift Over Time")
        if not drift_df.empty:
            df_plot = drift_df[columns].copy()
            df_plot["timestamp"] = drift_df.index
            fig = px.area(
                df_plot,
                x="timestamp",
                y=columns,
                title="📉 Drift Progression Over Time",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_traces(mode="lines+markers", hovertemplate="%{x}<br>%{y:.3f}")
            fig.update_layout(template="plotly_white", xaxis_title="Timestamp", yaxis_title="Drift Value")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No drift data yet. Run the pipeline first.")

    # ----- TAB 2: History -----
    with tab2:
        st.subheader("Recent Drift Runs")

        # Copy recent records and convert any dict objects to strings for display
        df_display = df_meta.tail(15).copy()
        df_display = df_display.applymap(lambda x: str(x) if isinstance(x, dict) else x)

        # Highlight only numeric columns (to avoid comparison errors)
        numeric_cols = df_display.select_dtypes(include=["number"]).columns

        st.dataframe(
            df_display.style.highlight_max(axis=0, subset=numeric_cols),
            use_container_width=True
        )

        st.download_button(
            "⬇️ Download Drift Log",
            df_meta.to_csv(index=False).encode(),
            "drift_log.csv",
            "text/csv"
        )

    # ----- TAB 3: Latest Data -----
    with tab3:
        st.subheader("Latest Dataset Snapshot")
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH)
            st.dataframe(df.head(25), use_container_width=True)
        else:
            st.warning("No dataset found.")
else:
    st.warning("⚠️ No drift logs available. Run drift_detector.py to populate metrics.")

# ---------- FOOTER ----------
st.markdown('<div class="footer">Made with ❤️ by Aayushi Waghela · Data Drift Watch Pro</div>', unsafe_allow_html=True)
