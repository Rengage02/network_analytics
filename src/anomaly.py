from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def fit_predict(self, df):
        try:
            if df is None or df.empty:
                raise ValueError("Input DataFrame is empty")

            features = df[["latency", "packet_size"]]
            df["anomaly"] = self.model.fit_predict(features)

            return df

        except Exception as e:
            print(f"❌ Anomaly detection error: {e}")
            return df