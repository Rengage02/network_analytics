import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        try:
            # 🔥 Use ENV variables (better practice)
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "network_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASS", "postgres"),
                host=os.getenv("DB_HOST", "52.66.87.148"),
                port=os.getenv("DB_PORT", "5432")
            )

            self.conn.autocommit = True  # 🔥 important for real-time inserts
            self.cursor = self.conn.cursor()

            print(f"✅ Connected to DB")

        except Exception as e:
            print("❌ DB Connection Error:", e)
            self.conn = None
            self.cursor = None

    def insert_data(self, row, anomaly=False, severity="NORMAL"):
        try:
            if not self.cursor:
                return

            query = """
            INSERT INTO network_data
            (timestamp, src_ip, dst_ip, packet_size, latency, protocol, packet_loss, anomaly, severity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(query, row + (anomaly, severity))

        except Exception as e:
            print("❌ Insert Error:", e)

    def fetch_data(self):
        try:
            if not self.cursor:
                return []

            self.cursor.execute(
                "SELECT * FROM network_data ORDER BY id DESC LIMIT 1000"
            )
            return self.cursor.fetchall()

        except Exception as e:
            print("❌ Fetch Error:", e)
            return []

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            print("🔌 DB connection closed")
        except Exception as e:
            print("❌ Close Error:", e)