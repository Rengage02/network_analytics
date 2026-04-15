import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class AlertService:
    def __init__(self):
        self.sender = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASS")
        self.receiver = self.sender

        self.last_sent_time = 0  # 🔥 NEW
        self.cooldown = 60  # seconds (1 min)

    def send_alert(self, message):
        import time

        current_time = time.time()

        # 🔥 Rate limiting
        if current_time - self.last_sent_time < self.cooldown:
            print("⏳ Alert skipped (cooldown active)")
            return

        try:
            if not self.sender or not self.password:
                print("⚠️ Email credentials missing")
                return

            msg = MIMEText(message)
            msg["Subject"] = "🚨 Network Alert"
            msg["From"] = self.sender
            msg["To"] = self.receiver

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender, self.password)
                server.send_message(msg)

            print("✅ Alert sent")

            # 🔥 update last sent time
            self.last_sent_time = current_time

        except Exception as e:
            print("❌ Alert failed:", e)