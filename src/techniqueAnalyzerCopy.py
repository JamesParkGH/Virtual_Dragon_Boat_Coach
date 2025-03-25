import sys
import os
import pandas as pd
import re
import math

from identifyPaddlingSide import identifyPaddlingSide
from strokeCounter import strokeCounter
from identifyPhase import identifyPhase
from dataPreprocessing import dataPreprocessing

from topArmAnalyzer import topArmAnalyzer
from bottomArmAnalyzer import bottomArmAnalyzer
from rotationAnalyzer import rotationAnalyzer
from paddleAngleAnalyzer import paddleAngleAnalyzer

from constants import *

def techniqueAnalyzer(trc_file, mot_file):
    right_side = identifyPaddlingSide(trc_file)

    mot_df, neck_x_index, top_wrist_x_index, top_shoulder_x_index, top_elbow_x_index, top_hip_x_index, top_knee_x_index, bottom_wrist_x_index, bottom_shoulder_x_index, bottom_elbow_x_index, bottom_hip_x_index, bottom_knee_x_index = dataPreprocessing(trc_file, mot_file)

    # track number of threshold violations
    # need to make sure not over counting -> only increment by 1 per cycle
    # need elapsed number of strokes
    stroke_count, stroke_frames = strokeCounter(trc_file)
    stroke_count -= 1   # Gives intervals instead of end markers

    stroke_phases = identifyPhase(trc_file)

    # Cannot exceed curr_stroke
    top_arm_count = 0
    top_arm_updated = False

    bottom_elbow_count = 0
    bottom_elbow_updated = False

    rotation_count = 0
    rotation_count_updated = False

    posture_count = 0
    hinge_lower_count = False
    hinge_upper_count = False
    posture_count_updated = False
    hinge_lower_updated = False
    hinge_upper_updated = False


    # # Paddle angle
    trc_df = pd.read_csv(trc_file, sep=",", engine="python", header=None)

    positive_frames = 0
    pull_frames = 0
    paddle_angle_ratios = []


    curr_stroke = 0
    
    # loop through df
    # Start at first full stroke (stroke_frames[0])
    for frame in range(len(stroke_frames)-1):
        # Track current frame range
        frame_l = stroke_frames[frame]
        frame_u = stroke_frames[frame+1]

        # Reset update indicators on each stroke
        top_arm_updated = False
        bottom_elbow_updated = False
        posture_count_updated = True

        # Check positive frame ratio
        # if frame > stroke_frames[0]:
        #     paddle_angle_ratios.append(positive_frames/pull_frames)

        positive_frames = 0
        pull_frames = 0

        # inc stroke count
        curr_stroke += 1


        ### Top Arm Analysis ###
        top_elbow_angle_count, top_ratio_count, elbow_hammer_count = topArmAnalyzer(trc_df, mot_df, frame_l, frame_u, stroke_phases, top_wrist_x_index, top_shoulder_x_index, top_elbow_x_index)

        if top_elbow_angle_count or top_ratio_count or elbow_hammer_count:
            top_arm_count += 1

    # NEW top arm
    # Top arm movement in x-axis during pull (top hand relative to top shoulder)
    # Elbow angle + arm rotation angular velocity
    # Height top hand over head?


        ### Bottom Arm Analysis ###
        bottom_elbow_angle_count, bottom_elbow_track_count = bottomArmAnalyzer(trc_df, mot_df, frame_l, frame_u, stroke_phases, bottom_elbow_x_index, bottom_wrist_x_index)

        if bottom_elbow_angle_count or bottom_elbow_track_count:
            bottom_elbow_count += 1

        ### Rotation Analysis ###
        fwd_rotation_count, bwd_rotation_count = rotationAnalyzer(trc_df, mot_df, frame_l, frame_u, bottom_shoulder_x_index, top_shoulder_x_index)

        if fwd_rotation_count or bwd_rotation_count:
            rotation_count += 1

        ### Paddle Angle Analysis ###
        positive_ratio = paddleAngleAnalyzer(trc_df, mot_df, stroke_phases, bottom_wrist_x_index, top_wrist_x_index)

    ##############################################################
    ### Analysis ###
    ##############################################################
    top_arm_score = top_arm_count/stroke_count
    
    bottom_arm_score = bottom_elbow_count/stroke_count

    rotation_score = rotation_count/stroke_count

    paddle_angle_score = positive_ratio
    
    return [top_arm_score, bottom_arm_score, rotation_score, paddle_angle_score]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python techniqueAnalyzer.py <trc_file> <mot_file>")
        sys.exit(1)

    trc_file = sys.argv[1]
    mot_file = sys.argv[2]

    scores = techniqueAnalyzer(trc_file, mot_file)
    print(scores)
