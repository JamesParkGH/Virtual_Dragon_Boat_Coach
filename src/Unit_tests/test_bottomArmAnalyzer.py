import unittest
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bottomArmAnalyzer import bottomArmAnalyzer
from dataPreprocessing import dataPreprocessing
from identifyPhase import identifyPhase

class TestBottomArmAnalyzer(unittest.TestCase):

    def setUp(self):
        self.trc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.mot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_mot.csv"))
        self.phase_list = identifyPhase(self.trc_path)
        self.trc_df = pd.read_csv(self.trc_path, sep=",", engine="python", header=None)
        self.mot_df, self.neck_x_index, self.top_wrist_x_index, self.top_shoulder_x_index, self.top_elbow_x_index, self.top_hip_x_index, self.top_knee_x_index, self.bottom_wrist_x_index, self.bottom_shoulder_x_index, self.bottom_elbow_x_index, self.bottom_hip_x_index, self.bottom_knee_x_index = dataPreprocessing(self.trc_path, self.mot_path)

    def test_normal_case(self):
        #Test normal function execution with valid input.
        angle_count, elbow_track_count = bottomArmAnalyzer(self.trc_df, self.mot_df, 1, 60, self.phase_list, self.bottom_elbow_x_index, self.bottom_wrist_x_index)
        self.assertFalse(angle_count)
        self.assertGreaterEqual(elbow_track_count, 0) 
    
    def test_no_recovery_phase(self):
        #Test when no recovery phase is present.
        stroke_phases_no_recovery = ["pull"] * 704
        self.assertRaises(ZeroDivisionError, bottomArmAnalyzer, self.trc_df, self.mot_df, 1, 60, stroke_phases_no_recovery, self.bottom_elbow_x_index, self.bottom_wrist_x_index)

    def test_empty_dataframe(self):
        #Test function behavior with empty DataFrames.
        empty_trc_df = pd.DataFrame()
        empty_mot_df = pd.DataFrame()
        self.assertRaises(KeyError, bottomArmAnalyzer, empty_trc_df, empty_mot_df, 1, 60, self.phase_list, self.bottom_elbow_x_index, self.bottom_wrist_x_index)
        self.assertRaises(KeyError, bottomArmAnalyzer, self.trc_df, empty_mot_df, 1, 60, self.phase_list, self.bottom_elbow_x_index, self.bottom_wrist_x_index)
        self.assertRaises(IndexError, bottomArmAnalyzer, empty_trc_df, self.mot_df, 1, 60, self.phase_list, self.bottom_elbow_x_index, self.bottom_wrist_x_index)

if __name__ == '__main__':
    unittest.main()
