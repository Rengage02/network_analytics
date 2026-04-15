import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import time
from src.data_generator import DataGenerator
from src.analytics import NetworkAnalytics
from src.anomaly import AnomalyDetector
from src.DB import Database
import pandas as pd
from src.alert import AlertService


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
            "packet_size", "latency", "protocol", "packet_loss"
        ])

        detector = AnomalyDetector()
        df = detector.fit_predict(df)

        return df

    except Exception as e:
        st.error(f"DB Error: {e}")
        return pd.DataFrame()


def main():
    st.title("📡 Network Operations Center Dashboard NOC")

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

    analytics = NetworkAnalytics(df)

    # 🔷 KPIs
    kpis = analytics.calculate_kpis()

    st.subheader("📊 KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Avg Latency", f"{kpis.get('avg_latency', 0):.2f} ms")
    col2.metric("Max Latency", f"{kpis.get('max_latency', 0):.2f} ms")
    col3.metric("Packets", kpis.get("total_packets", 0))
    col4.metric("Packet Loss %", f"{kpis.get('packet_loss_rate', 0):.2f}")

    # 🔷 Latency Chart
    st.subheader("📈 Latency Trend")
    st.line_chart(df["latency"])

    # 🔷 Protocol Chart
    st.subheader("🌐 Protocol Distribution")
    st.bar_chart(analytics.traffic_by_protocol())

    # 🔷 Top Talkers
    st.subheader("🔥 Top Talkers")
    st.dataframe(analytics.top_talkers())

    # 🔷 Anomaly Detection
    st.subheader("🚨 Anomaly Detection")

    if "anomaly" in df.columns:
        anomalies = df[(df["anomaly"] == -1) & (df["latency"] > latency_threshold)]
    else:
        anomalies = pd.DataFrame()

    alert = AlertService()

    if not anomalies.empty:
        st.error(f"{len(anomalies)} critical anomalies detected!")

        if "last_alert" not in st.session_state:
            st.session_state.last_alert = 0

        current_time = time.time()

        if current_time - st.session_state.last_alert > 60:
            alert.send_alert(f"{len(anomalies)} anomalies detected in network!")
            st.session_state.last_alert = current_time

        st.dataframe(anomalies.head(10))
    else:
        st.success("No critical anomalies")

    # 🔷 Raw Data
    with st.expander("📄 Raw Data"):
        st.dataframe(df.head(50))

    # 🔄 Auto refresh
    time.sleep(REFRESH_INTERVAL)
    st.rerun()


if __name__ == "__main__":
    main()