import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from strokeCounter import strokeCounter

class TestStrokeCounter(unittest.TestCase):

    def setUp(self):
        self.trc_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.trc_file_one = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc_one_stroke.csv"))
        self.trc_file_zero = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc_no_stroke.csv"))

    def test_basic_stroke_counting(self):
        #Test normal stroke counting in a normal trc file
        stroke_count, timestamps = strokeCounter(self.trc_file)
        expected_count = 10
        self.assertEqual(stroke_count, expected_count)
        self.assertEqual(len(timestamps), expected_count)

    def test_zero_stroke(self):
        #Test counting a file no stroke data.
        stroke_count, timestamps = strokeCounter(self.trc_file_zero)
        self.assertEqual(stroke_count, 0)
        self.assertEqual(len(timestamps), 0)

    def test_single_stroke(self):
        #Test counting a file with exactly one stroke.
        stroke_count, timestamps = strokeCounter(self.trc_file_one)
        self.assertEqual(stroke_count, 1)
        self.assertEqual(len(timestamps), 1)

    def test_invalid_file_format(self):
        #Test function behavior with an missing trc file.
        with self.assertRaises(SystemExit) as cm:
            print("\nIt is expected to see an message saying there is an Error reading file as the file does not exist")
            strokeCounter("non_existent.csv")
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
