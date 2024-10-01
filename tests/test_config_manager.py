# tests/test_config_manager.py

import unittest
from unittest.mock import patch, mock_open

from crontab import CronTab

from src.config_manager import ConfigManager

class TestConfigManager(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="[DEFAULT]\nLogFilePath=app.log\nInterval=0 1 * * *\n[EMAIL]\nSMTPServer=smtp.example.com\nSMTPPort=587\nFromAddress=from@example.com\nToAddress=to@example.com\nUsername=user\nPassword=pass")
    def setUp(self, mock_file):
        self.config_manager = ConfigManager()

    def test_get_log_file_path(self):
        self.assertEqual(self.config_manager.get_log_file_path(), 'app.log')

    @patch.object(CronTab, 'next', return_value=3600)
    @patch('configparser.ConfigParser.get', return_value='0 1 * * *')
    def test_interval_returns_correct_value(self, mock_get, mock_next):
        interval = self.config_manager.get_interval()
        self.assertEqual(interval, 3600)

    @patch.object(CronTab, 'next', return_value=0)
    @patch('configparser.ConfigParser.get', return_value='* * * * *')
    def test_interval_handles_every_minute(self, mock_get, mock_next):
        interval = self.config_manager.get_interval()
        self.assertEqual(interval, 0)

    @patch.object(CronTab, 'next', return_value=86400)
    @patch('configparser.ConfigParser.get', return_value='0 0 * * *')
    def test_interval_handles_every_day(self, mock_get, mock_next):
        interval = self.config_manager.get_interval()
        self.assertEqual(interval, 86400)

    @patch.object(CronTab, 'next', return_value=0)
    @patch('configparser.ConfigParser.get', return_value='invalid cron')
    def test_interval_handles_invalid_cron_expression(self, mock_get, mock_next):
        with self.assertRaises(ValueError):
            self.config_manager.get_interval()

    def test_log_file_path_returns_default_if_not_set(self):
        with patch('builtins.open', new_callable=mock_open, read_data="[DEFAULT]\nInterval=0 1 * * *\n[EMAIL]\nSMTPServer=smtp.example.com\nSMTPPort=587\nFromAddress=from@example.com\nToAddress=to@example.com\nUsername=user\nPassword=pass"):
            config_manager = ConfigManager()
            self.assertEqual(config_manager.get_log_file_path(), 'app.log')

    def test_log_file_path_returns_value_from_config(self):
        self.assertEqual(self.config_manager.get_log_file_path(), 'app.log')

    def test_smtp_server_returns_value_from_config(self):
        self.assertEqual(self.config_manager.get_smtp_server(), 'smtp.example.com')

    def test_smtp_port_returns_value_from_config(self):
        self.assertEqual(self.config_manager.get_smtp_port(), 587)

    def test_from_address_returns_value_from_config(self):
        self.assertEqual(self.config_manager.get_from_address(), 'from@example.com')

    def test_to_address_returns_value_from_config(self):
        self.assertEqual(self.config_manager.get_to_address(), 'to@example.com')

    def test_interval_returns_next_run_time(self):
        with patch('src.config_manager.CronTab.next', return_value=3600):
            self.assertEqual(self.config_manager.get_interval(), 3600)

    def test_log_file_path_returns_default_if_missing(self):
        with patch('builtins.open', new_callable=mock_open, read_data="[DEFAULT]\nInterval=0 1 * * *\n[EMAIL]\nSMTPServer=smtp.example.com\nSMTPPort=587\nFromAddress=from@example.com\nToAddress=to@example.com\nUsername=user\nPassword=pass"):
            config_manager = ConfigManager()
            self.assertEqual(config_manager.get_log_file_path(), 'app.log')

    def test_smtp_port_returns_default_if_missing(self):
        with patch('builtins.open', new_callable=mock_open, read_data="[DEFAULT]\nLogFilePath=app.log\nInterval=0 1 * * *\n[EMAIL]\nSMTPServer=smtp.example.com\nFromAddress=from@example.com\nToAddress=to@example.com\nUsername=user\nPassword=pass"):
            config_manager = ConfigManager()
            self.assertEqual(config_manager.get_smtp_port(), 25)

    def test_interval_returns_default_if_invalid(self):
        with patch('builtins.open', new_callable=mock_open, read_data="[DEFAULT]\nLogFilePath=app.log\nInterval=invalid\n[EMAIL]\nSMTPServer=smtp.example.com\nSMTPPort=587\nFromAddress=from@example.com\nToAddress=to@example.com\nUsername=user\nPassword=pass"):
            config_manager = ConfigManager()
            with self.assertRaises(ValueError):
                config_manager.get_interval()
if __name__ == '__main__':
    unittest.main()