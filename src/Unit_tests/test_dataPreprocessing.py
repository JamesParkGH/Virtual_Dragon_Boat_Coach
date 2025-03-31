import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dataPreprocessing import dataPreprocessing

class TestDataPreprocessing(unittest.TestCase):

    def setUp(self):
        self.trc_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.mot_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_mot.csv"))

    def test_data_processing(self):
        
        mot_df, neck_x_index, top_wrist_x, top_shoulder_x, top_elbow_x, top_hip_x, top_knee_x, bottom_wrist_x, bottom_shoulder_x, bottom_elbow_x, bottom_hip_x, bottom_knee_x = dataPreprocessing(self.trc_file, self.mot_file)

        #Test if renaming happened correctly
        for i in mot_df:
            self.assertIn("hip_flexion_bottom", mot_df.columns)
            self.assertIn("knee_angle_top", mot_df.columns)

        self.assertEqual(top_wrist_x, 20)
        self.assertEqual(top_shoulder_x, 14)
        self.assertEqual(top_elbow_x, 17)
        self.assertEqual(top_hip_x, 35)
        self.assertEqual(top_knee_x, 38)
        self.assertEqual(bottom_wrist_x, 11)
        self.assertEqual(bottom_shoulder_x, 5)
        self.assertEqual(bottom_elbow_x, 8)
        self.assertEqual(bottom_hip_x, 26)
        self.assertEqual(bottom_knee_x, 29)


    def test_missing_files(self):
        #Test Handling of missing or corrupted files
        with self.assertRaises(SystemExit) as cm:
            print("\nIt is expected to see an message saying there is an Error reading file as the file does not exist")
            dataPreprocessing("non_existent_trc.csv", self.mot_file)
        self.assertEqual(cm.exception.code, 1)

        self.assertRaises(FileNotFoundError, dataPreprocessing, self.trc_file, "non_existent_mot.csv")

        with self.assertRaises(SystemExit) as cm:
            print("\nIt is expected to see an message saying there is an Error reading file as the file does not exist")
            self.assertRaises(FileNotFoundError, dataPreprocessing, "non_existent_trc.csv", "non_existent_mot.csv")
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
