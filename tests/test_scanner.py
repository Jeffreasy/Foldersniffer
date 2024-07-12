import unittest
import os
from src.core.scanner import scan_directory
import logging

class TestScanner(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'test_dir'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, 'test_file.txt'), 'w') as f:
            f.write('This is a test file.')
        logging.info('Temporary directory and file created for testing.')

    def tearDown(self):
        os.remove(os.path.join(self.test_dir, 'test_file.txt'))
        os.rmdir(self.test_dir)
        logging.info('Temporary directory and file removed after testing.')

    def test_scan_directory(self):
        results = scan_directory(self.test_dir, [], [], [])
        logging.debug(f'Scan results: {results}')
        self.assertEqual(len(results), 1)

    def test_scan_with_exclusions(self):
        results = scan_directory(self.test_dir, ['test_file.txt'], [], [])
        logging.debug(f'Scan results with exclusions: {results}')
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
