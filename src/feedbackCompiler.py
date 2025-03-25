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
            'The elbow is also tracking outwards effectively, allowing for a better press off the back of your stroke.',
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
    feedback['improvement_points']['limiting_factors'] = ['Poor lat engagement','Unnecessary exertion during recovery ']
    feedback['improvement_points']['potential_injuries'] = ['Tenosynovitis', "Golfer's elbow"]
    feedback['improvement_points']['technical_feedback'] = [
        'Keep the angle in the bottom arm steady.',
        'Think about pulling downwards instead of pulling towards you. This will favour lat engagement over bicep engagement and help keep your arm straighter as you pull.',
        'You can also focus more on sitting up and derotating with your stroke. Imagine that your arms are just strings that attach to the paddle and generate your power by moving your body. Your arms should feel very relaxed throughout.',
        'Make sure to point the elbow outwards and relax the bottom wrist during your recovery. If you’re doing it properly, the elbow should be further away from your body than the hand holding the paddle. One cue is to imagine that you are wearing a wristwatch and are trying to point it forwards as your hand move from the back of your stroke to your A-frame.'
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Single arm lat pullovers (Or other exercises for engaging the lat with a straight arm)',
        'Cable Woodchoppers',
        'Landmine Rotations'
    ]

def generate_rotation_feedback(score):
    feedback = {
        'category': 'Rotation',
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
    
    if score <= ROTATION_GOOD_SCORE:
        feedback['rating'] = 'Good'
        feedback['main_points'] = [
            'You are rotating well with your stroke. This helps you keep consistent pressure on your blade as you pull. ',
            'Don\'t forget to keep thinking about sitting up along with your rotation to maximize the use of your body. '
        ]
    elif score <= ROTATION_BAD_SCORE:
        feedback['rating'] = 'Moderate'
        feedback['main_points'] = [
            'Your rotation is decent, but it seems there are still some restrictions in your range of motion.',
            'Having better range of motion as you rotate into your catch will increase the length of your stroke without the need to “over-reach”. This sets you up with more potential to de-rotate as you pull to add torque to your stroke.'
        ]
        add_rotation_improvement_points(feedback)
    else:
        feedback['rating'] = 'Bad'
        feedback['main_points'] = [
            'Your rotation at your catch is very limited. Your shoulders are too square when they should be somewhat staggered and stacked. ',
            'Having limited range of motion in your rotation prevents you from generating torque by using your bodyweight. It will also force you to “over-reach” to gain get more length, leading you to fight against your natural range of motion with every stroke and increase your risk of injury.'
        ]
        add_rotation_improvement_points(feedback)
    
    return feedback

def add_rotation_improvement_points(feedback):
    feedback['improvement_points']['limiting_factors'] = [
        'Limited thoracic rotation',
        'Limited hip mobility',
        'Lower back tightness'
    ]
    feedback['improvement_points']['potential_injuries'] = ['Lower back pain']
    feedback['improvement_points']['technical_feedback'] = [
        'Rotation and de-rotation should be initiated at the hips, not by twisting from the upper back. Allow your paddle-side shoulder and hip to move forward together as you catch and move back together as you drive off your leg and sit up when pulling.',
        'When going forwards into your catch, imagine the paddling side of your body swinging open like a door. Your torso should move as a single unit without any twisting. You should notice that your paddle-side knee bends slightly, meaning that your hip has come forward. As you enter your catch, imagine that you are trying to show your upper back to someone watching you from the side; they should be able to see your top shoulder clearly.',
        'When working on your rotation, don\'t think too hard about needing to reach as far as you can with your arms. Reaching only with your arms will cause poor posture. Find a range of motion where you can comfortably keep your chest upright while getting your body forwards instead. '
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Landmine Rotations',
        'Seated Wall Angels',
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
    if score <= POSITIVE_ANGLE_SCORE:
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
        'Another cause of the paddle angle becoming negative too quickly is from not sitting up enough as you pull. By moving your body up and back throughout the stroke, your bottom hand can stay in front of you for longer to maintain a positive angle. Note that you should be trying to find pressure on your paddle by sitting up first, rather pulling with your arms immediately after catching.'
    ]
    feedback['improvement_points']['corrective_exercises'] = [
        'Kettlebell Windmills',
        'Butt Walks',
        'Cable Woodchoppers',
        'Kettlebell Hip Shift'
    ]

def compile_feedback(scores):
    # Take 4 scores from the technique analyzer
    top_arm_upper_score, bottom_elbow_upper_score, rotation_score, paddle_angle_score = scores
    
    # Generate feedback for each area
    feedback = {
        'top_arm': generate_top_arm_feedback(top_arm_upper_score),
        'bottom_arm': generate_bottom_arm_feedback(bottom_elbow_upper_score),
        'rotation': generate_rotation_feedback(rotation_score), 
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