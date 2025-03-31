import unittest
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from techniqueAnalyzer import techniqueAnalyzer
from identifyPhase import identifyPhase
from dataPreprocessing import dataPreprocessing

class TestTechniqueAnalyzer(unittest.TestCase):

    def setUp(self):
        self.trc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.mot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_mot.csv"))
        self.phase_list = identifyPhase(self.trc_path)
        self.trc_df = pd.read_csv(self.trc_path, sep=",", engine="python", header=None)
        self.mot_df, self.neck_x_index, self.top_wrist_x_index, self.top_shoulder_x_index, self.top_elbow_x_index, self.top_hip_x_index, self.top_knee_x_index, self.bottom_wrist_x_index, self.bottom_shoulder_x_index, self.bottom_elbow_x_index, self.bottom_hip_x_index, self.bottom_knee_x_index = dataPreprocessing(self.trc_path, self.mot_path)

    def test_normal_case(self):
        #Test normal execution with valid data.
        scores = techniqueAnalyzer(self.trc_path, self.mot_path)
        self.assertEqual(len(scores), 4)
        for score in scores:
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 1)
        
    def test_no_strokes(self):
        #Test when strokeCounter detects no strokes.
        no_stroke_trc = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc_no_stroke.csv"))
        scores = techniqueAnalyzer(no_stroke_trc, self.mot_path)
        self.assertEqual(scores, [0, 0, 0, 0])

    def test_extreme_rotation(self):
        #Test unrealistic rotation and coordinate
        ex_rotation_trc = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc_rotation.csv"))
        scores = techniqueAnalyzer(ex_rotation_trc, self.mot_path)
        self.assertEqual(scores[2], 1)
    
    def test_empty_files(self):
        #Test when input files are empty.
        empty_trc = "empty_trc.csv"
        empty_mot = "empty_mot.csv"
        with self.assertRaises(SystemExit) as cm:
            print("\nIt is expected to see an message saying there is an Error reading file as the test input file does not exist")
            techniqueAnalyzer(empty_trc, empty_mot)
        self.assertEqual(cm.exception.code, 1)
        
        self.assertRaises(FileNotFoundError, techniqueAnalyzer, self.trc_path, empty_mot)

        with self.assertRaises(SystemExit) as cm:
            print("\nIt is expected to see an message saying there is an Error reading file as the test input file does not exist")
            techniqueAnalyzer(empty_trc, self.mot_path)
        self.assertEqual(cm.exception.code, 1)

if __name__ == "__main__":
    unittest.main()