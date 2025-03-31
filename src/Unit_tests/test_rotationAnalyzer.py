import unittest
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from rotationAnalyzer import rotationAnalyzer
from dataPreprocessing import dataPreprocessing
from identifyPhase import identifyPhase

class TestRotationAnalyzer(unittest.TestCase):

    def setUp(self):
        self.trc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.mot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_mot.csv"))
        self.trc_df = pd.read_csv(self.trc_path, sep=",", engine="python", header=None)
        self.mot_df, self.neck_x_index, self.top_wrist_x_index, self.top_shoulder_x_index, self.top_elbow_x_index, self.top_hip_x_index, self.top_knee_x_index, self.bottom_wrist_x_index, self.bottom_shoulder_x_index, self.bottom_elbow_x_index, self.bottom_hip_x_index, self.bottom_knee_x_index = dataPreprocessing(self.trc_path, self.mot_path)

    def test_normal_case_farward_rotation(self):
        #Test normal function execution with valid forward rotation input.
        front_rot, back_rot = rotationAnalyzer(self.trc_df, self.mot_df, 1, 60, self.bottom_shoulder_x_index, self.top_shoulder_x_index)
        self.assertEqual(front_rot, 0)
        self.assertEqual(back_rot, 0) 
    
    def test_normal_case_back_rotation(self):
        #Test normal function execution with valid backward rotation input.
        self.trc_path_rot = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc_rotation.csv"))
        self.trc_df_rot = pd.read_csv(self.trc_path_rot, sep=",", engine="python", header=None)
        self.mot_df, self.neck_x_index, self.top_wrist_x_index, self.top_shoulder_x_index, self.top_elbow_x_index, self.top_hip_x_index, self.top_knee_x_index, self.bottom_wrist_x_index, self.bottom_shoulder_x_index, self.bottom_elbow_x_index, self.bottom_hip_x_index, self.bottom_knee_x_index = dataPreprocessing(self.trc_path_rot, self.mot_path)
        
        front_rot, back_rot = rotationAnalyzer(self.trc_df_rot, self.mot_df, 1, 60, self.bottom_shoulder_x_index, self.top_shoulder_x_index)
        self.assertEqual(front_rot, 1)
        self.assertEqual(back_rot, 1) 

    def test_empty_dataframe(self):
        #Test function behavior with empty DataFrames.
        empty_trc_df = pd.DataFrame()
        empty_mot_df = pd.DataFrame()
        self.assertRaises(IndexError, rotationAnalyzer, empty_trc_df, empty_mot_df, 1, 60, self.bottom_shoulder_x_index, self.top_shoulder_x_index)
        front_rot, back_rot = rotationAnalyzer(self.trc_df, empty_mot_df, 1, 60, self.bottom_shoulder_x_index, self.top_shoulder_x_index)
        self.assertRaises(IndexError, rotationAnalyzer, empty_trc_df, self.mot_df, 1, 60, self.bottom_shoulder_x_index, self.top_shoulder_x_index)

if __name__ == '__main__':
    unittest.main()
