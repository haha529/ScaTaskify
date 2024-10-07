# tests/test_scheduler.py

import unittest
from unittest.mock import patch

from config_manager import ConfigManager
from scheduler import Scheduler
from sync_service import SyncService


class TestScheduler(unittest.TestCase):
    def test_scheduler_initialization(self):
        scheduler = Scheduler()
        self.assertIsNotNone(scheduler.sync_service)

    @patch.object(ConfigManager, 'get_interval', return_value=3600)
    @patch.object(SyncService, 'sync')
    @patch('time.sleep', return_value=None)
    def test_scheduler_runs_sync_service(self, mock_sleep, mock_sync, mock_get_interval):
        scheduler = Scheduler()
        scheduler.start(iterations=1)
        mock_sync.assert_called_once()
        mock_sleep.assert_called_once_with(3600)

    @patch.object(ConfigManager, 'get_interval', return_value=0)
    @patch.object(SyncService, 'sync')
    @patch('time.sleep', return_value=None)
    def test_scheduler_handles_zero_interval(self, mock_sleep, mock_sync, mock_get_interval):
        scheduler = Scheduler()
        scheduler.start(iterations=1)
        mock_sync.assert_called_once()
        mock_sleep.assert_called_once_with(0)

    @patch.object(ConfigManager, 'get_interval', return_value=-1)
    @patch.object(SyncService, 'sync')
    @patch('time.sleep', return_value=None)
    def test_scheduler_handles_negative_interval(self, mock_sleep, mock_sync, mock_get_interval):
        scheduler = Scheduler()
        scheduler.start(iterations=1)
        mock_sync.assert_called_once()
        mock_sleep.assert_called_once_with(-1)

if __name__ == '__main__':
    unittest.main()