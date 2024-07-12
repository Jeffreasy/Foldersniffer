import unittest
from PyQt6.QtWidgets import QApplication
from src.ui.dialogs.settings_dialog import SettingsDialog
import logging

class TestSettingsDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.dialog = SettingsDialog()
        logging.info('SettingsDialog created for testing.')

    def test_initialization(self):
        self.assertEqual(self.dialog.windowTitle(), "Settings")
        logging.debug('Dialog title checked: Settings')

    def test_save_settings(self):
        self.dialog.save_settings()
        logging.debug('Settings saved.')

if __name__ == '__main__':
    unittest.main()
