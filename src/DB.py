import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="network_db",
                user="postgres",
                password="postgres",
                host="host.docker.internal",  # important for Docker
                port="5432"
            )
            self.cursor = self.conn.cursor()
            print("✅ DB Connected")
        except Exception as e:
            print("❌ DB Connection Error:", e)

    def insert_data(self, row):
        try:
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
            self.cursor.execute(
                "SELECT * FROM network_data ORDER BY id DESC LIMIT 1000"
            )
            return self.cursor.fetchall()
        except Exception as e:
            print("❌ Fetch Error:", e)
            return []