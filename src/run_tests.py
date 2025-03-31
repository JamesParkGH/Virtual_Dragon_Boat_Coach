import unittest
import os
import sys
if os.path.exists(os.path.abspath(os.path.dirname(__file__))):
        os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Running all the unit tests
if __name__ == "__main__":
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("Unit_tests")

    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)