import unittest
import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from constants import *
from feedbackCompiler import *

class TestfeedbackCompilerTopArm(unittest.TestCase):

    def test_TA_good_score(self):
        #Test that feedback is correct for a good score
        score = TOP_ARM_GOOD_SCORE
        feedback = generate_top_arm_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Good')
        self.assertIn('Your top arm looks good.', feedback['main_points'][0])
        self.assertIn('Keep working on the pressing motion and following through with your stroke.', feedback['main_points'][1])
        
        # Check that no improvement points are added
        self.assertEqual(feedback['improvement_points'], {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        })

    def test_TA_moderate_score(self):
        #Test that feedback is correct for a moderate score
        score = TOP_ARM_BAD_SCORE
        feedback = generate_top_arm_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Moderate')
        self.assertIn('Your top arm is somewhat bent during your stroke.', feedback['main_points'][0])
        self.assertIn('keep the arm as straight as possible to maximize your leverage.', feedback['main_points'][1])
        self.assertIn('when recovering (returning to A-frame) as well for better efficiency.', feedback['main_points'][2])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['potential_injuries']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)

    def test_TA_bad_score(self):
        #Test that feedback is correct for a bad score
        score = TOP_ARM_BAD_SCORE + 0.01
        feedback = generate_top_arm_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Bad')
        self.assertIn('Your top arm is too bent during your stroke.', feedback['main_points'][0])
        self.assertIn('to maximize your leverage.', feedback['main_points'][1])
        self.assertIn('Your arm needs to remain straight when recovering', feedback['main_points'][2])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['potential_injuries']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)

    def test_TA_feedback_structure(self):
        #Test that the feedback dictionary structure is correct
        score = 0.5
        feedback = generate_top_arm_feedback(score)
        
        # Check the structure of the feedback dictionary
        self.assertIn('category', feedback)
        self.assertEqual('Top Arm',feedback['category'])
        self.assertIn('rating', feedback)
        self.assertIn('score', feedback)
        self.assertEqual(score,feedback['score'])
        self.assertIn('main_points', feedback)
        self.assertIn('improvement_points', feedback)

        # Check improvement points structure
        self.assertIn('limiting_factors', feedback['improvement_points'])
        self.assertIn('potential_injuries', feedback['improvement_points'])
        self.assertIn('technical_feedback', feedback['improvement_points'])
        self.assertIn('corrective_exercises', feedback['improvement_points'])

        
class TestfeedbackCompilerBottomArm(unittest.TestCase):

    def test_BA_good_score(self):
        #Test that feedback is correct for a good score
        score = BOTTOM_ARM_GOOD_SCORE
        feedback = generate_bottom_arm_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Good')
        self.assertIn('Your bottom arm looks good.', feedback['main_points'][0])
        self.assertIn('The elbow is also tracking outwards effectively', feedback['main_points'][1])
        self.assertIn('at the front of your stroke and derotating as you pull to generate power', feedback['main_points'][2])
        
        # Check that no improvement points are added
        self.assertEqual(feedback['improvement_points'], {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        })

    def test_BA_moderate_score(self):
        #Test that feedback is correct for a moderate score
        score = BOTTOM_ARM_BAD_SCORE
        feedback = generate_bottom_arm_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Moderate')
        self.assertIn('Your bottom arm is bending a bit much when you pull.', feedback['main_points'][0])
        self.assertIn('This is an issue for longer duration efforts where you smaller muscles (biceps, triceps)', feedback['main_points'][1])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['potential_injuries']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)

    def test_BA_bad_score(self):
        #Test that feedback is correct for a bad score
        score = BOTTOM_ARM_BAD_SCORE + 0.01
        feedback = generate_bottom_arm_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Bad')
        self.assertIn('Your bottom arm is bending too much when you pull.', feedback['main_points'][0])
        self.assertIn('Bending the arm when pulling indicates that you are trying to generate power with your arms rather than your body and larger muscles.', feedback['main_points'][1])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['potential_injuries']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)

    def test_BA_feedback_structure(self):
        #Test that the feedback dictionary structure is correct
        score = 0.5
        feedback = generate_bottom_arm_feedback(score)
        
        # Check the structure of the feedback dictionary
        self.assertIn('category', feedback)
        self.assertEqual('Bottom Arm',feedback['category'])
        self.assertIn('rating', feedback)
        self.assertIn('score', feedback)
        self.assertEqual(score,feedback['score'])
        self.assertIn('main_points', feedback)
        self.assertIn('improvement_points', feedback)

        # Check improvement points structure
        self.assertIn('limiting_factors', feedback['improvement_points'])
        self.assertIn('potential_injuries', feedback['improvement_points'])
        self.assertIn('technical_feedback', feedback['improvement_points'])
        self.assertIn('corrective_exercises', feedback['improvement_points'])

class TestfeedbackCompilerRotation(unittest.TestCase):

    def test_RT_good_score(self):
        #Test that feedback is correct for a good score
        score = ROTATION_GOOD_SCORE
        feedback = generate_rotation_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Good')
        self.assertIn('You are rotating well with your stroke.', feedback['main_points'][0])
        self.assertIn('forget to keep thinking about sitting up along with', feedback['main_points'][1])
        
        # Check that no improvement points are added
        self.assertEqual(feedback['improvement_points'], {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        })

    def test_RT_moderate_score(self):
        #Test that feedback is correct for a moderate score
        score = ROTATION_BAD_SCORE
        feedback = generate_rotation_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Moderate')
        self.assertIn('there are still some restrictions in your range of motion.', feedback['main_points'][0])
        self.assertIn('better range of motion as you rotate into your catch will increase', feedback['main_points'][1])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['potential_injuries']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)

    def test_RT_bad_score(self):
        #Test that feedback is correct for a bad score
        score = ROTATION_BAD_SCORE + 0.01
        feedback = generate_rotation_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Bad')
        self.assertIn('Your rotation at your catch is very limited', feedback['main_points'][0])
        self.assertIn('Having limited range of motion in your rotation prevents you from', feedback['main_points'][1])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['potential_injuries']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)

    def test_RT_feedback_structure(self):
        #Test that the feedback dictionary structure is correct
        score = 0.5
        feedback = generate_rotation_feedback(score)
        
        # Check the structure of the feedback dictionary
        self.assertIn('category', feedback)
        self.assertEqual('Rotation',feedback['category'])
        self.assertIn('rating', feedback)
        self.assertIn('score', feedback)
        self.assertEqual(score,feedback['score'])
        self.assertIn('main_points', feedback)
        self.assertIn('improvement_points', feedback)

        # Check improvement points structure
        self.assertIn('limiting_factors', feedback['improvement_points'])
        self.assertIn('potential_injuries', feedback['improvement_points'])
        self.assertIn('technical_feedback', feedback['improvement_points'])
        self.assertIn('corrective_exercises', feedback['improvement_points'])

class TestfeedbackCompilerPaddleAngle(unittest.TestCase):

    def test_PA_good_score(self):
        #Test that feedback is correct for a good score
        score = POSITIVE_ANGLE_SCORE
        feedback = generate_paddle_angle_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Good')
        self.assertIn('You are maintaining a positive angle very well throughout your stroke.', feedback['main_points'][0])
        self.assertIn('This means that the force you are producing will be effectively applied when moving the boat.', feedback['main_points'][1])
        
        # Check that no improvement points are added
        self.assertEqual(feedback['improvement_points'], {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        })

    def test_PA_moderate_score(self):
        #Test that feedback is correct for a moderate score
        score = 0.7
        feedback = generate_paddle_angle_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Moderate')
        self.assertIn('Your paddle angle is positive for part of your stroke but becomes negative a little too soon.', feedback['main_points'][0])
        self.assertIn('A negative paddle angle applies force in a way', feedback['main_points'][1])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)
        # Check that no potential injuries are added to paddle angle feedback
        self.assertEqual(feedback['improvement_points']['potential_injuries'], [])

    def test_PA_bad_score(self):
        #Test that feedback is correct for a bad score
        score = 0.701
        feedback = generate_paddle_angle_feedback(score)
        
        # Check the rating and main points
        self.assertEqual(feedback['rating'], 'Bad')
        self.assertIn('Your paddle angle is becoming negative too quickly.', feedback['main_points'][0])
        self.assertIn('It also makes it more difficult to apply you bodyweight', feedback['main_points'][1])
        
        # Check that improvement points are added
        self.assertGreater(len(feedback['improvement_points']['limiting_factors']), 0)
        self.assertGreater(len(feedback['improvement_points']['technical_feedback']), 0)
        self.assertGreater(len(feedback['improvement_points']['corrective_exercises']), 0)
        # Check that no potential injuries are added to paddle angle feedback
        self.assertEqual(feedback['improvement_points']['potential_injuries'], [])

    def test_PA_feedback_structure(self):
        #Test that the feedback dictionary structure is correct
        score = 0.5
        feedback = generate_paddle_angle_feedback(score)
        
        # Check the structure of the feedback dictionary
        self.assertIn('category', feedback)
        self.assertEqual('Paddle Angle',feedback['category'])
        self.assertIn('rating', feedback)
        self.assertIn('score', feedback)
        self.assertEqual(score,feedback['score'])
        self.assertIn('main_points', feedback)
        self.assertIn('improvement_points', feedback)

        # Check improvement points structure
        self.assertIn('limiting_factors', feedback['improvement_points'])
        self.assertIn('potential_injuries', feedback['improvement_points'])
        self.assertIn('technical_feedback', feedback['improvement_points'])
        self.assertIn('corrective_exercises', feedback['improvement_points'])

if __name__ == "__main__":
    unittest.main()
