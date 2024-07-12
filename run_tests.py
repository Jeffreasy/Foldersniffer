import unittest
import logging
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the PYTHONPATH to include the src directory
sys.path.insert(0, os.path.abspath(os.getenv('PYTHONPATH')))

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if not result.wasSuccessful():
        logging.error('Tests failed.')
    else:
        logging.info('All tests passed.')

if __name__ == '__main__':
    run_tests()
