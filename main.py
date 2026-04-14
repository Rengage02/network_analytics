from src.data_generator import DataGenerator
from src.analytics import NetworkAnalytics
from src.anomaly import AnomalyDetector


def main():
    try:
        # Step 1: Generate Data
        generator = DataGenerator(rows=1000)
        df = generator.generate()
        generator.save_to_csv(df)

        if df is None:
            raise ValueError("Data generation failed")

        # Step 2: Anomaly Detection
        detector = AnomalyDetector()
        df = detector.fit_predict(df)

        # Step 3: Analytics
        analytics = NetworkAnalytics(df)

        kpis = analytics.calculate_kpis()
        protocol_stats = analytics.traffic_by_protocol()
        top_ips = analytics.top_talkers()

        # Step 4: Output
        print("\n=== KPI SUMMARY ===")
        for k, v in kpis.items():
            print(f"{k}: {v}")

        print("\n=== Traffic by Protocol ===")
        print(protocol_stats)

        print("\n=== Top Talkers ===")
        print(top_ips)

        print("\n=== Anomalies ===")
        print(df[df["anomaly"] == -1].head())

    except Exception as e:
        print(f"🚨 Critical error in main: {e}")


if __name__ == "__main__":
    main()