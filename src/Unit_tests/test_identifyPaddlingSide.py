import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from identifyPaddlingSide import identifyPaddlingSide

class TestIdentifyPaddlingSide(unittest.TestCase):

    def setUp(self):
        self.trc_right_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.trc_left_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_left_trc.csv"))

    def test_side_identification(self):
        # Test if correct side is identified
        right_result = identifyPaddlingSide(self.trc_right_path)
        left_result = identifyPaddlingSide(self.trc_left_path)
        self.assertTrue(right_result)
        self.assertTrue(not left_result)

    def test_missing_file(self):
        # Test Handling of missing file
        with self.assertRaises(SystemExit) as cm:
            print("\nIt is expected to see an message saying there is an Error reading file as the file does not exist")
            identifyPaddlingSide("non_existent.csv")
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
