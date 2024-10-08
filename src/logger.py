# src/logger.py

import logging
from config_manager import ConfigManager

class Logger:
    def __init__(self):
        config = ConfigManager()
        log_file_path = config.get_log_file_path()

        logging.basicConfig(filename=log_file_path, level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()

    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

