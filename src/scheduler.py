# src/scheduler.py

import time
from sync_service import SyncService
from config_manager import ConfigManager

class Scheduler:
    def __init__(self):
        self.sync_service = SyncService()
        self.config_manager = ConfigManager()

    def start(self, iterations=None):
        count = 0
        while True:
            self.sync_service.sync()
            interval = self.config_manager.get_interval()
            time.sleep(interval)
            if iterations is not None:
                count += 1
                if count >= iterations:
                    break