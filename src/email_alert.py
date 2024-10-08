# src/email_alert.py

import smtplib
from email.mime.text import MIMEText

from logger import Logger
from config_manager import ConfigManager

class EmailAlert:
    def __init__(self):
        config = ConfigManager()
        self.smtp_server = config.get_smtp_server()
        self.smtp_port = config.get_smtp_port()
        self.from_addr = config.get_from_address()
        self.to_addr = config.get_to_address()
        self.logger = Logger()

    def send_email_alert(self, message):
        msg = MIMEText(message)
        msg['Subject'] = 'Error Alert'
        msg['From'] = self.from_addr
        msg['To'] = self.to_addr

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")

