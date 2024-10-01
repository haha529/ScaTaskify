# tests/test_logger.py

import unittest
from unittest import skipIf
from unittest.mock import patch, MagicMock
from src.logger import Logger

class TestLogger(unittest.TestCase):
    @patch('src.logger.ConfigManager')
    @patch('src.logger.logging')
    def test_error_logs_message(self, mock_logging, mock_config_manager):
        mock_config_manager.return_value.get_log_file_path.return_value = 'app.log'
        logger = Logger()
        logger.error('Error message')
        mock_logging.getLogger().error.assert_called_once_with('Error message')

    @patch('src.logger.ConfigManager')
    @patch('src.logger.logging')
    def test_info_logs_message(self, mock_logging, mock_config_manager):
        mock_config_manager.return_value.get_log_file_path.return_value = 'app.log'
        logger = Logger()
        logger.info('Info message')
        mock_logging.getLogger().info.assert_called_once_with('Info message')

    @patch('src.logger.ConfigManager')
    @patch('src.logger.logging')
    def test_debug_logs_message(self, mock_logging, mock_config_manager):
        mock_config_manager.return_value.get_log_file_path.return_value = 'app.log'
        logger = Logger()
        logger.debug('Debug message')
        mock_logging.getLogger().debug.assert_called_once_with('Debug message')

    @patch('src.logger.ConfigManager')
    @patch('src.logger.logging')
    def test_warning_logs_message(self, mock_logging, mock_config_manager):
        mock_config_manager.return_value.get_log_file_path.return_value = 'app.log'
        logger = Logger()
        logger.warning('Warning message')
        mock_logging.getLogger().warning.assert_called_once_with('Warning message')

    @patch('src.logger.ConfigManager')
    @patch('src.logger.logging')
    def test_critical_logs_message(self, mock_logging, mock_config_manager):
        mock_config_manager.return_value.get_log_file_path.return_value = 'app.log'
        logger = Logger()
        logger.critical('Critical message')
        mock_logging.getLogger().critical.assert_called_once_with('Critical message')


if __name__ == '__main__':
    unittest.main()