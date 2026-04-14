import pandas as pd
import random
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.DB import Database

class DataGenerator:
    def __init__(self, rows=1000):
        self.rows = rows

    def generate(self):
        try:
            data = []
            base_time = datetime.now()

            for i in range(self.rows):
                timestamp = base_time + timedelta(seconds=i)

                src_ip = f"192.168.1.{random.randint(1, 255)}"
                dst_ip = f"10.0.0.{random.randint(1, 255)}"

                packet_size = random.randint(64, 1500)
                latency = random.gauss(50, 10)

                if random.random() < 0.05:
                    latency = random.randint(150, 300)

                protocol = random.choice(["TCP", "UDP"])
                packet_loss = 1 if random.random() < 0.02 else 0

                row = (
                    timestamp, src_ip, dst_ip,
                    packet_size, latency,
                    protocol, packet_loss
                )

                data.append(row)

            # 🔥 INSERT INTO DB
            db = Database()
            for row in data:
                db.insert_data(row)

            print("✅ Data inserted into DB")

            return pd.DataFrame(data, columns=[
                "timestamp", "src_ip", "dst_ip",
                "packet_size", "latency",
                "protocol", "packet_loss"
            ])

        except Exception as e:
            print(f"❌ Error generating data: {e}")
            return None

    def save_to_csv(self, df, path="data/network_data.csv"):
        try:
            if df is None:
                raise ValueError("DataFrame is empty")

            df.to_csv(path, index=False)
            print("✅ Data saved to CSV")

        except Exception as e:
            print(f"❌ Error saving CSV: {e}")