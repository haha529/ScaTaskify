# tests/test_sync_service.py

import unittest
from src.sync_service import SyncService

class TestSyncService(unittest.TestCase):
    def test_sync(self):
        sync_service = SyncService()
        self.assertIsNone(sync_service.sync())

if __name__ == '__main__':
    unittest.main()