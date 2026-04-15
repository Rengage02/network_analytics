import time
import random
from datetime import datetime
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class DataGenerator:
    LOG_FILE = os.path.join(BASE_DIR, "data", "router.log")

    def __init__(self, delay=1):
        self.delay = delay  # seconds between logs

    def generate_log(self):
        # Current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simulated network fields
        src_ip = f"192.168.1.{random.randint(1, 255)}"
        dst_ip = f"10.0.0.{random.randint(1, 255)}"

        packet_size = random.randint(64, 1500)
        latency = round(random.gauss(50, 10), 2)

        # Inject anomaly (latency spike)
        if random.random() < 0.1:
            latency = random.randint(150, 300)

        protocol = random.choice(["TCP", "UDP"])
        packet_loss = 1 if random.random() < 0.05 else 0

        # Final log format
        log = (
            f"{timestamp} "
            f"SRC={src_ip} DST={dst_ip} "
            f"SIZE={packet_size} LAT={latency} "
            f"PROTO={protocol} LOSS={packet_loss}"
        )

        return log

    def run(self):
        print("📡 Generating real-time logs... (Press CTRL+C to stop)")

        # Ensure data folder exists
        os.makedirs("data", exist_ok=True)

        while True:
            log = self.generate_log()

            # Write to log file
            with open(self.LOG_FILE, "a") as f:
                f.write(log + "\n")

            # Print for visibility
            print("Generated:", log)
            print("Writing to:", self.LOG_FILE)
            # Wait before next log
            time.sleep(self.delay)


if __name__ == "__main__":
    generator = DataGenerator(delay=1)
    generator.run()