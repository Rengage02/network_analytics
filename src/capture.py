import time
import re
import os
from src.DB import Database
from src.anomaly import AnomalyDetector
from src.alert import AlertService


class LogCapture:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.log_file = os.path.join(self.base_dir, "data", "router.log")

    def follow(self, file):
        """Continuously read new lines (like tail -f)"""
        file.seek(0, 2)

        while True:
            line = file.readline()

            if not line:
                time.sleep(0.5)
                continue

            yield line.strip()

    def parse_log(self, line):
        """Parse log line into structured data"""
        try:
            match = re.search(
                r"(.*?) SRC=(.*?) DST=(.*?) SIZE=(\d+) LAT=(\d+\.?\d*) PROTO=(\w+) LOSS=(\d+)",
                line
            )

            if not match:
                return None

            return {
                "timestamp": match.group(1),
                "src_ip": match.group(2),
                "dst_ip": match.group(3),
                "packet_size": int(match.group(4)),
                "latency": float(match.group(5)),
                "protocol": match.group(6),
                "packet_loss": int(match.group(7))
            }

        except Exception as e:
            print("❌ Parse error:", e)
            return None

    def run(self):
        print("📡 Listening to router.log...")

        if not os.path.exists(self.log_file):
            print("❌ Log file not found:", self.log_file)
            return

        db = Database()
        detector = AnomalyDetector()
        alert = AlertService()

        with open(self.log_file, "r") as file:
            for line in self.follow(file):
                parsed = self.parse_log(line)

                if not parsed:
                    continue

                # 🔥 ANOMALY DETECTION
                is_anomaly, severity = detector.detect(parsed)

                # 🔥 ALERT TRIGGER
                if is_anomaly and severity=="HIGH":
                    alert.send_alert(
                        f"""
            🚨 Network Alert

            Severity: {severity}
            Latency: {parsed['latency']}
            Packet Loss: {parsed['packet_loss']}
            Source IP: {parsed['src_ip']}
            """
                    )

                # 🔥 INSERT INTO DB
                row = (
                    parsed["timestamp"],
                    parsed["src_ip"],
                    parsed["dst_ip"],
                    parsed["packet_size"],
                    parsed["latency"],
                    parsed["protocol"],
                    parsed["packet_loss"]
                )

                db.insert_data(row, is_anomaly, severity)

                print(f"✅ Inserted | Anomaly: {is_anomaly} | Severity: {severity}")


if __name__ == "__main__":
    capture = LogCapture()
    capture.run()