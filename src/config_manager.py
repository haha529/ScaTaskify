# src/config_manager.py

import configparser
from crontab import CronTab


class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_log_file_path(self):
        log_file_name = self.config['DEFAULT'].get('LogFilePath', 'app.log')
        return log_file_name

    def get_smtp_server(self):
        return self.config['EMAIL'].get('SMTPServer', fallback='localhost')

    def get_smtp_port(self):
        return self.config['EMAIL'].getint('SMTPPort', fallback=25)

    def get_from_address(self):
        return self.config['EMAIL'].get('FromAddress')

    def get_to_address(self):
        return self.config['EMAIL'].get('ToAddress')

    def get_interval(self):
        cron_expression = self.config['DEFAULT'].get('Interval', '0 1 * * *')
        cron = CronTab(cron_expression)
        next_run = cron.next(default_utc=True)
        return next_run
