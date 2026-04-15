import psycopg2
import os

class Database:
    def __init__(self):
        try:
            # 🔥 Use EC2 DB everywhere
            host = "52.66.87.148"

            self.conn = psycopg2.connect(
                dbname="network_db",
                user="postgres",
                password="postgres",
                host=host,
                port="5432"
            )

            self.cursor = self.conn.cursor()
            print(f"✅ Connected to EC2 DB: {host}")

        except Exception as e:
            print("❌ DB Connection Error:", e)
            self.conn = None
            self.cursor = None

    def insert_data(self, row):
        try:
            if not self.cursor:
                return

            query = """
            INSERT INTO network_data
            (timestamp, src_ip, dst_ip, packet_size, latency, protocol, packet_loss)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, row)
            self.conn.commit()

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