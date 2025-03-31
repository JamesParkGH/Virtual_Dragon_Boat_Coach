import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from identifyPhase import identifyPhase

class TestIdentifyPhase(unittest.TestCase):

    def setUp(self):
        self.trc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc.csv"))
        self.trc_file_one = os.path.abspath(os.path.join(os.path.dirname(__file__), "Test_trc_one_stroke.csv"))

    def test_normal_phase_identification(self):
        #Test normal phase identifying with a valid trc file.
        phase_list = identifyPhase(self.trc_path)
        self.assertEqual(len(phase_list), 704)
        self.assertEqual(phase_list[10], "pull")
        self.assertEqual(phase_list[50], "recovery")
        self.assertEqual(phase_list[90], "pull")
        self.assertEqual(phase_list[130], "recovery")

    def test_single_stroke_cycle(self):
        #Test phase detection of a single pull and recovery cycle.
        phase_list = identifyPhase(self.trc_file_one)
        self.assertIn("pull", phase_list)
        self.assertIn("recovery", phase_list)
        self.assertIn("None", phase_list)

    def test_invalid_file_format(self):
        #Test function behavior with an invalid trc file.
        phase_list = identifyPhase("non_existent.csv")
        for i in phase_list:
            self.assertEqual(i,"None")

if __name__ == '__main__':
    unittest.main()
