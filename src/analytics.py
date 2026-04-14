class NetworkAnalytics:
    def __init__(self, df):
        self.df = df

    def calculate_kpis(self):
        try:
            return {
                "avg_latency": self.df["latency"].mean(),
                "max_latency": self.df["latency"].max(),
                "min_latency": self.df["latency"].min(),
                "total_packets": len(self.df),
                "packet_loss_rate": self.df["packet_loss"].mean() * 100
            }
        except Exception as e:
            print(f"❌ KPI calculation error: {e}")
            return {}

    def traffic_by_protocol(self):
        try:
            return self.df["protocol"].value_counts()
        except Exception as e:
            print(f"❌ Protocol analysis error: {e}")
            return None

    def top_talkers(self, n=5):
        try:
            return self.df["src_ip"].value_counts().head(n)
        except Exception as e:
            print(f"❌ Top talkers error: {e}")
            return None