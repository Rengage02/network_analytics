import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import time
from src.analytics import NetworkAnalytics
from src.DB import Database
import pandas as pd


st.set_page_config(page_title="Network NOC Dashboard", layout="wide")


# 🔄 Auto refresh
REFRESH_INTERVAL = 5  # seconds

@st.cache_data(ttl=5)
def load_data():
    try:
        db = Database()
        data = db.fetch_data()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=[
            "id", "timestamp", "src_ip", "dst_ip",
            "packet_size", "latency", "protocol", "packet_loss",
            "anomaly", "severity"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        return df

    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()


def main():
    st.title("📡 Network Operations Center Dashboard NOC")
    st.caption(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Sidebar filters
    st.sidebar.header("⚙️ Filters")

    protocol_filter = st.sidebar.multiselect(
        "Select Protocol",
        options=["TCP", "UDP"],
        default=["TCP", "UDP"]
    )

    latency_threshold = st.sidebar.slider(
        "Latency Threshold (ms)",
        50, 300, 150
    )
    df = load_data()

    if df.empty:
        st.warning("⚠️ No data available")
        return

    # Apply filters
    df = df[df["protocol"].isin(protocol_filter)]
    filtered_df = df[df["latency"] >= latency_threshold]


    analytics = NetworkAnalytics(df)

    # 🔷 KPIs
    kpis = analytics.calculate_kpis()
    st.subheader("📊 KPIs")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Latency", f"{kpis.get('avg_latency', 0):.2f} ms")
    col2.metric("Max Latency", f"{kpis.get('max_latency', 0):.2f} ms")
    col3.metric("Packets", kpis.get("total_packets", 0))
    col4.metric("Packet Loss %", f"{kpis.get('packet_loss_rate', 0):.2f}")
    col5 = st.columns(5)[-1]
    col5.metric("Anomalies", len(df[df["anomaly"] == True]))
    # THEN show severity
    st.subheader("📊 Severity Distribution")
    st.bar_chart(df["severity"].value_counts())
    # 🔷 Latency Chart
    st.subheader("📈 Latency Trend")
    df_sorted = df.sort_values("timestamp")
    st.line_chart(df_sorted.set_index("timestamp")["latency"])

    # 🔷 Protocol Chart
    st.subheader("🌐 Protocol Distribution")
    st.bar_chart(analytics.traffic_by_protocol())

    # 🔷 Top Talkers
    st.subheader("🔥 Top Talkers")
    st.dataframe(analytics.top_talkers())

    st.subheader("🚨 Alerts")
    # 🔴 Critical
    critical = filtered_df[filtered_df["severity"] == "HIGH"].sort_values(by="timestamp", ascending=False)
    warning = filtered_df[filtered_df["severity"] == "MEDIUM"].sort_values(by="timestamp", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        if len(critical) > 0:
            st.error(f"🔴 Critical Issues: {len(critical)}")
        else:
            st.success("🟢 No critical issues")
        if not critical.empty:
            st.dataframe(critical.head(5), use_container_width=True)

    with col2:
        st.warning(f"🟡 Warnings: {len(warning)}")
        if not warning.empty:
            st.dataframe(warning.head(5), use_container_width=True)

    # 🔷 Raw Data
    with st.expander("📄 Raw Data"):
        st.dataframe(df.head(50))

    # 🔄 Auto refresh
    time.sleep(REFRESH_INTERVAL)
    st.rerun()


if __name__ == "__main__":
    main()