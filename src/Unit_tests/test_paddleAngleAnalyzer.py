import unittest
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from paddleAngleAnalyzer import paddleAngleAnalyzer
from dataPreprocessing import dataPreprocessing
from identifyPhase import identifyPhase

class TestPaddleAngleAnalyzer(unittest.TestCase):

    def setUp(self):
        self.trc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.mot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_mot.csv"))
        self.phase_list = identifyPhase(self.trc_path)
        self.trc_df = pd.read_csv(self.trc_path, sep=",", engine="python", header=None)
        self.mot_df, self.neck_x_index, self.top_wrist_x_index, self.top_shoulder_x_index, self.top_elbow_x_index, self.top_hip_x_index, self.top_knee_x_index, self.bottom_wrist_x_index, self.bottom_shoulder_x_index, self.bottom_elbow_x_index, self.bottom_hip_x_index, self.bottom_knee_x_index = dataPreprocessing(self.trc_path, self.mot_path)

    def test_normal_case(self):
        #Test normal execution with valid trc and mot.
        positive_ratio, negative_count = paddleAngleAnalyzer(self.trc_df, self.mot_df, 1, 60, self.phase_list, self.bottom_wrist_x_index, self.top_wrist_x_index)
        self.assertGreaterEqual(positive_ratio, 0)
        self.assertLessEqual(positive_ratio, 1)
        self.assertGreaterEqual(negative_count, 0)

    def test_no_pull_phase(self):
        #Test when no pull phase is present.
        stroke_phases_no_pull = ["recovery"] * 704
        self.assertRaises(ZeroDivisionError, paddleAngleAnalyzer, self.trc_df, self.mot_df, 1, 60, stroke_phases_no_pull, self.bottom_wrist_x_index, self.top_wrist_x_index)

    def test_empty_dataframe(self):
        #Test function behavior with empty DataFrames.
        empty_trc_df = pd.DataFrame()
        empty_mot_df = pd.DataFrame()
        self.assertRaises(IndexError, paddleAngleAnalyzer, empty_trc_df, empty_mot_df, 1, 60, self.phase_list, self.bottom_wrist_x_index, self.top_wrist_x_index)
        self.assertRaises(KeyError, paddleAngleAnalyzer, self.trc_df, empty_mot_df, 1, 60, self.phase_list, self.bottom_wrist_x_index, self.top_wrist_x_index)
        self.assertRaises(IndexError, paddleAngleAnalyzer, empty_trc_df, self.mot_df, 1, 60, self.phase_list, self.bottom_wrist_x_index, self.top_wrist_x_index)

if __name__ == '__main__':
    unittest.main()
