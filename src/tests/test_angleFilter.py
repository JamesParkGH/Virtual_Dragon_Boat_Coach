import unittest
import os
import sys
from unittest.mock import patch, mock_open
from scipy.ndimage import gaussian_filter1d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from angleFilter import get_available_angles, plot_angle

class TestangleFilter(unittest.TestCase):
    
    @patch("builtins.open", new_callable=mock_open, read_data="frame,time,angle1,angle2\n1,0,-0.393,0.843\n2,0.017,-0.377,0.833\n3,0.033,-0.376,0.826\n")
    def test_get_available_angles_correct_angle_name(self, mock_file):
        #Test if get_available_angles correctly extracts angle names excluding 'time'.
        angles = get_available_angles("dummy.csv")
        self.assertEqual(angles, ["angle1", "angle2"])

    @patch("builtins.open", new_callable=mock_open, read_data="frame,time, ,angle2\n1,0, ,0.843\n2,0.017, ,0.833\n3,0.033, ,0.826\n")
    def test_get_available_angles_missing_columns(self, mock_file):
        #Test if get_available_angles correctly extracts angle names when empty column present
        angles = get_available_angles("dummy.csv")
        self.assertEqual(angles, [" ", "angle2"])

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_get_available_angles_empty_file(self, mock_file):
        #Test if get_available_angles handles an empty file input
        with self.assertRaises(StopIteration):  # next() should fail
            get_available_angles("dummy.csv")

    def test_get_available_angles_file_missing(self):
        #Test if function raises an error for a missing file input
        with self.assertRaises(FileNotFoundError):
            get_available_angles("nonexistent.csv")

    @patch("builtins.open", new_callable=mock_open, read_data="frame,time,angle1,angle2\n1,0,-0.393,0.843\n2,0.017,-0.377,0.833\n3,0.033,-0.376,0.826\n")
    def test_plot_angle_request_angle_missing(self, mock_file):
        #Test if plot_angle raises KeyError when the requested angle is missing
        with self.assertRaises(KeyError):
            plot_angle("dummy.csv", "angle3")

    def test_plot_angle_no_file(self):
        #Test if plot_angle raises an error for a missing file.
        with self.assertRaises(FileNotFoundError):
            plot_angle("nodummy.csv", "angle1")

if __name__ == "__main__":
    unittest.main()
