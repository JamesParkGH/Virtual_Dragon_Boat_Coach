from constants import *

def generate_top_arm_feedback(score):
    feedback = {
        'category': 'Top Arm',
        'rating': '',
        'score': score,
        'main_points': [],
        'improvement_points': {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        }
    }
    
    if score <= TOP_ARM_GOOD_SCORE:
        feedback['rating'] = 'Good'
        feedback['main_points'] = [
            'Your top arm looks good. You are doing a good job of keeping it straight to maximize your leverage.',
            'Keep working on the pressing motion and following through with your stroke.'
        ]
    elif score <= TOP_ARM_BAD_SCORE:
        feedback['rating'] = 'Moderate'
        feedback['main_points'] = [
            'Your top arm is somewhat bent during your stroke. Though not excessive, there is still room for improvement.',
            'Your goal is to keep the arm as straight as possible to maximize your leverage.',
            'Your arm needs to remain straight when recovering (returning to A-frame) as well for better efficiency.'
        ]
        add_top_arm_improvement_points(feedback)
    else:
        feedback['rating'] = 'Bad'
        feedback['main_points'] = [
            'Your top arm is too bent during your stroke. You will see in your paddling videos that your hand is too close to your forehead.',
            'Your goal is to keep the arm as straight as possible to maximize your leverage.',
            'Your arm needs to remain straight when recovering (returning to A-frame) as well for better efficiency.'
        ]
        add_top_arm_improvement_points(feedback)
    
    return feedback

def add_top_arm_improvement_points(feedback):
    feedback['improvement_points']['limiting_factors'] = [
        'Poor range of motion in the shoulder',
        'Limited range of motion in rotation of the trunk'
    ]
    feedback['improvement_points']['potential_injuries'] = ['Subacromial Impingement']
    feedback['improvement_points']['technical_feedback'] = [
        'Think of your top hand and elbow moving together',
        "Imagine there is a straight bar from your hand to your shoulder, so don't hammer the elbow and focus more on pressing down",
        'Try to rotate more as well. This will allow you to keep your arm straight as you set up in your A-frame and keep your hand away from your forehead'
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Shoulder External Rotation',
        'Kettlebell Windmills',
        'Cable Pullovers'
    ]

def generate_bottom_arm_feedback(score):
    feedback = {
        'category': 'Bottom Arm',
        'rating': '',
        'score': score,
        'main_points': [],
        'improvement_points': {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        }
    }
    
    if score <= BOTTOM_ARM_GOOD_SCORE:
        feedback['rating'] = 'Good'
        feedback['main_points'] = [
            'Your bottom arm looks good. You are keeping the angle steady which implies that your lats are engaged.',
            'Keep thinking about rotating at the front of your stroke and derotating as you pull to generate power. This also ties into emphasizing hinging and sitting up.'
        ]
    elif score <= BOTTOM_ARM_BAD_SCORE:
        feedback['rating'] = 'Moderate'
        feedback['main_points'] = [
            'Your bottom arm is bending a bit much when you pull. A slight bend is acceptable but try to keep the angle steady throughout.',
            'Bending the arm when pulling indicates that you are trying to generate power with your arms rather than your body and larger muscles. This is an issue for longer duration efforts where you smaller muscles (biceps, triceps) will fatigue very quickly, lowering your output.'
        ]
        add_bottom_arm_improvement_points(feedback)
    else:
        feedback['rating'] = 'Bad'
        feedback['main_points'] = [
            'Your bottom arm is bending too much when you pull. A slight bend is acceptable but try to keep the angle steady throughout.',
            'Bending the arm when pulling indicates that you are trying to generate power with your arms rather than your body and larger muscles. This is an issue for longer duration efforts where you smaller muscles (biceps, triceps) will fatigue very quickly, lowering your output.'
        ]
        add_bottom_arm_improvement_points(feedback)
    
    return feedback

def add_bottom_arm_improvement_points(feedback):
    feedback['improvement_points']['limiting_factors'] = ['Poor lat engagement']
    feedback['improvement_points']['potential_injuries'] = ['Tenosynovitis', "Golfer's elbow"]
    feedback['improvement_points']['technical_feedback'] = [
        'Keep the angle in the bottom arm steady.',
        'Think about pulling downwards instead of pulling towards you. This will favour lat engagement over bicep engagement and help keep your arm straighter as you pull.',
        'You can also focus more on sitting up and derotating with your stroke. Imagine that your arms are just strings that attach to the paddle and generate your power by moving your body. Your arms should feel very relaxed throughout.'
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Single arm lat pullovers (Or other exercises for engaging the lat with a straight arm)',
        'Cable Woodchoppers',
        'Landmine Rotations'
    ]

def generate_posture_feedback(score):
    feedback = {
        'category': 'Posture',
        'rating': '',
        'score': score,
        'main_points': [],
        'improvement_points': {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        }
    }
    
    if score <= POSTURE_GOOD_SCORE:
        feedback['rating'] = 'Good'
        feedback['main_points'] = [
            'Your hip hinge looks good. You are effectively using your range of motion to take long and powerful strokes.',
            'Don\'t forget to keep thinking about implementing rotation along with your hinge to maximize your efficiency'
        ]
    elif score <= POSTURE_BAD_SCORE:
        feedback['rating'] = 'Moderate'
        feedback['main_points'] = [
            'Your posture is decent, but it seems there are still some restrictions in your hinge range of motion.',
            'Having better range of motion in your hips will help you generate more power in each stroke through sitting up and using your bodyweight. This is a more efficient use of energy and will help your endurance.'
        ]
        add_posture_improvement_points(feedback)
    else:
        feedback['rating'] = 'Bad'
        feedback['main_points'] = [
            'Your posture when paddling is too stiff. This noticeable through a limited ability to hinge forwards along with lots of bending in your lower back.',
            'Having limited range of motion in your hinge prevents you from generating power by using your bodyweight. It will also decrease the efficiency of your energy expenditure since you will need to fight against your natural range of motion with every stroke.'
        ]
        add_posture_improvement_points(feedback)
    
    return feedback

def add_posture_improvement_points(feedback):
    feedback['improvement_points']['limiting_factors'] = [
        'Hamstring tightness',
        'Limited hip mobility',
        'Lower back tightness'
    ]
    feedback['improvement_points']['potential_injuries'] = ['Lower back pain']
    feedback['improvement_points']['technical_feedback'] = [
        'The hinging motion should be initiated at the hips, not by bending from the lower back. Your spine should remain as neutral as possible when hinging forwards.',
        'When going forwards into your catch, imagine a string pulling you from your belly button bring you forwards while keeping your chin up. This will naturally help keep the chest open instead of crunched downwards to maintain the neutral spine throughout',
        'When working on your hinge, don\'t think too hard about needing to reach as far as you can with your arms. Reaching only with your arms will cause poor posture. Find a range of motion where you can comfortably keep your chest upright while getting your body forwards instead.'
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Romanian Deadlifts',
        'Pike Compressions (hip flexor strength)',
        'Kettlebell Hip Shift',
        'Elephant Walks'
    ]

def generate_paddle_angle_feedback(score):
    feedback = {
        'category': 'Paddle Angle',
        'rating': '',
        'score': score,
        'main_points': [],
        'improvement_points': {
            'limiting_factors': [],
            'potential_injuries': [],
            'technical_feedback': [],
            'corrective_exercises': []
        }
    }
    
    # Use constants for the thresholds
    if score > POSITIVE_ANGLE_SCORE:
        feedback['rating'] = 'Good'
        feedback['main_points'] = [
            'You are maintaining a positive angle very well throughout your stroke.',
            'This means that the force you are producing will be effectively applied when moving the boat.'
        ]
    elif score >= 0.085:  # This value could also be moved to constants.py
        feedback['rating'] = 'Moderate'
        feedback['main_points'] = [
            'Your paddle angle is positive for part of your stroke but becomes negative a little too soon.',
            'A negative paddle angle applies force in a way that pulls the boat downwards. It also makes it more difficult to apply your bodyweight when pressing through your stroke.'
        ]
        add_paddle_angle_improvement_points(feedback)
    else:
        feedback['rating'] = 'Bad'
        feedback['main_points'] = [
            'Your paddle angle is becoming negative too quickly.',
            'A negative paddle angle applies force in a way that pulls the boat downwards. It also makes it more difficult to apply you bodyweight when pressing through your stroke.'
        ]
        add_paddle_angle_improvement_points(feedback)
    
    return feedback

def add_paddle_angle_improvement_points(feedback):
    feedback['improvement_points']['limiting_factors'] = [
        'Minimal Rotation',
        'Not sitting up soon enough while pulling',
        'Pulling with the arms instead of using the body'
    ]
    feedback['improvement_points']['technical_feedback'] = [
        'Having the paddle angle become negative too quickly is related to aspects of rotation and derotation',
        'If you are not rotated enough at the catch, your paddle angle will be closer to being neutral or negative as you begin pulling. Think about turning your torso as you recover so your top shoulder stays back to force rotation as you enter your A-frame. Another cue is to imagine that there is someone watching you paddle from the side, and you are trying to show them your entire back.',
        'Another cause of the paddle angle becoming negative too quickly is from not sitting up enough as you pull. By moving your body back throughout the stroke, your bottom hand can stay in front of you for longer to maintain a positive angle.'
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Kettlebell Windmills',
        'Butt Walks',
        'Cable Woodchoppers',
        'Kettlebell Hip Shift'
    ]

def compile_feedback(scores):
    # Take 4 scores from the technique analyzer
    top_arm_upper_score, bottom_elbow_upper_score, posture_score, paddle_angle_score = scores
    
    # Generate feedback for each area
    feedback = {
        'top_arm': generate_top_arm_feedback(top_arm_upper_score),
        'bottom_arm': generate_bottom_arm_feedback(bottom_elbow_upper_score),
        'posture': generate_posture_feedback(posture_score),
        'paddle_angle': generate_paddle_angle_feedback(paddle_angle_score)
    }
    
    return feedback

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:  # Program name + 4 scores
        print("Usage: python feedbackCompiler.py <top_arm_score> <bottom_elbow_score> <posture_score> <paddle_angle_score>")
        sys.exit(1)
        
    scores = [float(score) for score in sys.argv[1:5]]
    feedback = compile_feedback(scores)
    print(feedback)