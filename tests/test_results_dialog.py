import unittest
from PyQt6.QtWidgets import QApplication
from src.ui.dialogs.results_dialog import ResultsDialog
import logging

class TestResultsDialog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.dialog = ResultsDialog([])
        logging.info('ResultsDialog created for testing.')

    def test_display_results(self):
        results = [{"path": "test_file.txt", "size": 20, "last_modified": "Mon Jan 01 00:00:00 2000", "created": "Mon Jan 01 00:00:00 2000", "mode": "-rw-r--r--", "owner": 1000}]
        self.dialog.load_results(results)
        self.assertEqual(self.dialog.tree.topLevelItemCount(), 1)
        logging.debug('Results displayed in dialog.')

if __name__ == '__main__':
    unittest.main()
