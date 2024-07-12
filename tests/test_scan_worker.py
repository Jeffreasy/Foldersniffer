import unittest
import os
from src.ui.workers.scan_worker import ScanWorker
import logging

class TestScanWorker(unittest.TestCase):
    def setUp(self):
        self.worker = ScanWorker("test_dir", [], [], [])
        logging.info('ScanWorker created for testing.')

    def test_worker_initialization(self):
        self.assertEqual(self.worker.directory, "test_dir")
        logging.debug('Worker directory checked: test_dir')

    def test_run(self):
        self.worker.run()
        logging.debug('ScanWorker run method executed.')

if __name__ == '__main__':
    unittest.main()
