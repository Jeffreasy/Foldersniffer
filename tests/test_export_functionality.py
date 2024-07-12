import unittest
import os
import shutil
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import FolderSnifferUI
import json
import zipfile

class TestExportFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.window = FolderSnifferUI()
        self.test_output_dir = os.path.join(os.path.dirname(__file__), 'test_output')
        if not os.path.exists(self.test_output_dir):
            os.makedirs(self.test_output_dir)
        self.window.output_dir_selector.input.setText(self.test_output_dir)

    def tearDown(self):
        shutil.rmtree(self.test_output_dir)

    def test_export_as_json(self):
        self.window.scan_results = [
            {"path": "file1.txt", "size": 100, "last_modified": "2024-07-11 02:00:00", "created": "2024-07-11 01:00:00", "mode": "0o100666", "owner": 0, "num_lines": 10, "num_chars": 100}
        ]
        self.window.export_as_json()
        json_path = os.path.join(self.test_output_dir, 'scan_results.json')
        self.assertTrue(os.path.exists(json_path))
        with open(json_path, 'r') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['path'], 'file1.txt')

    def test_export_as_txt(self):
        self.window.scan_results = [
            {"path": "file1.txt", "size": 100, "last_modified": "2024-07-11 02:00:00", "created": "2024-07-11 01:00:00", "mode": "0o100666", "owner": 0, "num_lines": 10, "num_chars": 100}
        ]
        self.window.export_as_txt()
        txt_path = os.path.join(self.test_output_dir, 'scan_results.txt')
        self.assertTrue(os.path.exists(txt_path))
        with open(txt_path, 'r') as f:
            content = f.read()
            self.assertIn('file1.txt', content)
            self.assertIn('Size: 100', content)

    def test_export_as_zip(self):
        self.window.scan_results = [
            {"path": "file1.txt", "size": 100, "last_modified": "2024-07-11 02:00:00", "created": "2024-07-11 01:00:00", "mode": "0o100666", "owner": 0, "num_lines": 10, "num_chars": 100}
        ]
        self.window.export_as_zip()
        zip_path = os.path.join(self.test_output_dir, 'scan_results.zip')
        self.assertTrue(os.path.exists(zip_path))
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            self.assertIn('scan_results.json', zipf.namelist())
            self.assertIn('scan_results.txt', zipf.namelist())

if __name__ == "__main__":
    unittest.main()
