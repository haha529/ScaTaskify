import requests

from logger import Logger
from email_alert import EmailAlert

class APIHandler:
    def __init__(self):
        self.logger = Logger()
        self.email_alert = EmailAlert()

    def call_api(self, url, params):
        try:
            print(url)
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API call failed: {e}")
            self.email_alert.send_email_alert(f"API call failed: {e}")
            return None