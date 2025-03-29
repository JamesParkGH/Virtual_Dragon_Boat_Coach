import unittest
import os
import sys
from unittest.mock import patch, mock_open
from scipy.ndimage import gaussian_filter1d
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from techniqueAnalyzer import techniqueAnalyzer

class TesttechniqueAnalyzer(unittest.TestCase):

    @patch("builtins.open")
    def test_get_available_angles_empty_file(self, mock_open):
        #Test if techniqueAnalyzer raises an error for a missing file.
        mock_file_1 = mock_open(read_data="").return_value
        mock_file_2 = mock_open(read_data="").return_value
        mock_open.side_effect = [mock_file_1, mock_file_2]

        with self.assertRaises(TypeError):
            techniqueAnalyzer("dummy1.trc","dummy2.mot")

    def test_techniqueAnalyzer_no_file(self):
        #Test if techniqueAnalyzer raises an error for a missing file.
        with self.assertRaises(FileNotFoundError):
            techniqueAnalyzer("nodummy1.trc", "nodummy2.mot")


if __name__ == "__main__":
    unittest.main()