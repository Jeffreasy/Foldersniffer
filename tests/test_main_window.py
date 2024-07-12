import unittest
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import FolderSnifferUI
import logging

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = FolderSnifferUI()
        logging.info('FolderSnifferUI created for testing.')

    def test_initialization(self):
        self.assertEqual(self.window.windowTitle(), "FolderSniffer")
        logging.debug('Window title checked: FolderSniffer')

    def test_scan_directory(self):
        self.window.scan_dir_selector.input.setText("test_dir")
        self.window.start_scan()
        self.assertTrue(hasattr(self.window, 'scan_worker') and self.window.scan_worker.isRunning())
        logging.debug('Scan worker is running.')

if __name__ == '__main__':
    unittest.main()
