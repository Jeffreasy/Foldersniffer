import unittest
from src.core.utils import get_file_info

class TestUtils(unittest.TestCase):
    def test_get_file_info(self):
        file_info = get_file_info(__file__)
        self.assertIn('size', file_info)
        self.assertIn('last_modified', file_info)
        self.assertIn('created', file_info)
        self.assertIn('mode', file_info)
        self.assertIn('owner', file_info)
        self.assertIn('num_lines', file_info)
        self.assertIn('num_chars', file_info)

    def test_get_file_info_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            get_file_info("non_existent_file.txt")

if __name__ == '__main__':
    unittest.main()
