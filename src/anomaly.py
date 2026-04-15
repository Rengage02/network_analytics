# src/anomaly.py

class AnomalyDetector:
    def __init__(self):
        pass

    def detect(self, data):
        """
        data = {
            latency,
            packet_loss,
            packet_size
        }
        """

        latency = data.get("latency", 0)
        packet_loss = data.get("packet_loss", 0)

        # 🔥 Rule-based detection
        if latency > 150:
            return True, "HIGH"

        if packet_loss > 0:
            return True, "MEDIUM"

        return False, "NORMAL"