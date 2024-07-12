import unittest
import os
import tempfile
from src.core.utils import get_file_info
import logging

class TestGetFileInfo(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file.write(b'Line 1\nLine 2\nLine 3')
        self.test_file.close()
        logging.info('Temporary file created for testing.')

    def tearDown(self):
        os.remove(self.test_file.name)
        logging.info('Temporary file removed after testing.')

    def test_get_file_info(self):
        file_info = get_file_info(self.test_file.name)
        logging.debug(f'File info: {file_info}')
        self.assertEqual(file_info['num_chars'], 21)  # Pas deze waarde aan op basis van de werkelijke inhoud
        self.assertEqual(file_info['num_lines'], 3)
        self.assertEqual(file_info['path'], self.test_file.name)

if __name__ == '__main__':
    unittest.main()
