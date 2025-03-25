import sys
import os
import pandas as pd
import re
import math

from identifyPaddlingSide import identifyPaddlingSide
from strokeCounter import strokeCounter
from identifyPhase import identifyPhase
from dataPreprocessing import dataPreprocessing

from topArmAnalyzer import *

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
    for frame in range(stroke_frames[0], stroke_frames[-1]):

    # track timeframe of threshold violations (start and stop)
        if frame in stroke_frames:

            # Reset update indicators on each stroke
            top_arm_updated = False
            bottom_elbow_updated = False
            posture_count_updated = True

            # Posture/hinge check
            # if hinge_lower_count and hinge_upper_count:
            #     posture_count += 1

            # hinge_lower_count = False
            # hinge_upper_count = False

            # Check positive frame ratio
            if frame > stroke_frames[0]:
                paddle_angle_ratios.append(positive_frames/pull_frames)

            positive_frames = 0
            pull_frames = 0

            # inc stroke count
            curr_stroke += 1


    # Top arm UPPER threshold check (top flex, top add, top rot)
        # if top_arm_updated==False and 180-mot_df['arm_flex_top'].values[frame] > TOP_ARM_FLEX_THRESHOLD and 180-mot_df['arm_add_top'].values[frame] < TOP_ARM_ADD_THRESHOLD and 180-mot_df['arm_rot_top'].values[frame] > TOP_ARM_ROT_THRESHOLD and 180-mot_df['elbow_flex_top'].values[frame] < TOP_ELBOW_THRESHOLD:
        #     top_arm_count += 1
        #     top_arm_updated = True

        if top_arm_updated==False:
            top_elbow_count, top_ratio_count = topArmAnalyzer(trc_df, mot_df, frame, top_wrist_x_index, top_shoulder_x_index)

            if top_elbow_count + top_ratio_count > 0:
                top_arm_count += 1
                top_arm_updated = True

    # NEW top arm
    # Top arm movement in x-axis during pull (top hand relative to top shoulder)
    # Elbow angle + arm rotation angular velocity
    # Height top hand over head?


    # Bottom arm UPPER threshold check (bottom elbow)
        if bottom_elbow_updated==False and 180-mot_df['elbow_flex_bottom'].values[frame] < BOTTOM_ELBOW_THRESHOLD:
            bottom_elbow_count += 1
            bottom_elbow_updated = True

    # Bottom arm LOWER threshold check (bottom elbow)


    # Spine posture threshold check (lumbar extension, bending)
    # Incorporate hip hinge -> should get lower than 70 degrees
        if posture_count_updated==False and 180-mot_df['lumbar_extension'].values[frame] > LUMBAR_EXTENSION_THRESHOLD and 180-mot_df['lumbar_bending'].values[frame] < LUMBAR_BENDING_THRESHOLD:
            # if hip_hinge_updated==False and 180-mot_df['hip_flexion_top'].values[frame] < 70 and 180-mot_df['hip_flexion_bottom'].values[frame] < 70:
            #     hip_hinge_count += 1
            #     hip_hinge_updated = True
            posture_count += 1
            posture_count_updated = True
        
        # if hinge_lower_updated==False and 180-mot_df['hip_flexion_top'].values[frame] < HIP_FLEXION_THRESHOLD and 180-mot_df['hip_flexion_bottom'].values[frame] < HIP_FLEXION_THRESHOLD and 180-mot_df['lumbar_bending'].values[frame] > LUMBAR_BENDING_THRESHOLD:
        #     hinge_lower_count = True

        # if hinge_upper_updated==False and 180-mot_df['hip_flexion_top'].values[frame] > 105 and 180-mot_df['hip_flexion_bottom'].values[frame] > 105:# and 180-mot_df['lumbar_bending'].values[frame] < LUMBAR_BENDING_THRESHOLD:
        #     hinge_upper_count = True


    # Track number of pulling frames
        if stroke_phases[frame] == "pull":
            pull_frames += 1
    # Paddle angle threshold check (trc_file: top/bottom wrist x+y components)
    # Duration of angle being positive (time ratio between positive_frames:total_frames)
        x_diff = trc_df.iloc[:,top_wrist_x_index].iloc[frame] - trc_df.iloc[:,bottom_wrist_x_index].iloc[frame]
        y_diff = trc_df.iloc[:,top_wrist_x_index+1].iloc[frame] - trc_df.iloc[:,bottom_wrist_x_index+1].iloc[frame]
        theta = math.degrees(math.atan(y_diff/x_diff))
        if theta <= 10 and stroke_phases[frame]=="pull":
            positive_frames += 1

    ##############################################################
    # Analysis
    ##############################################################
    top_arm_upper_score = top_arm_count/stroke_count
    
    bottom_elbow_upper_score = bottom_elbow_count/stroke_count
    
    posture_score = (stroke_count-posture_count)/stroke_count

    paddle_angle_score = sum(paddle_angle_ratios)/stroke_count
    return [top_arm_upper_score, bottom_elbow_upper_score, posture_score, paddle_angle_score]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python techniqueAnalyzer.py <trc_file> <mot_file>")
        sys.exit(1)

    trc_file = sys.argv[1]
    mot_file = sys.argv[2]

    scores = techniqueAnalyzer(trc_file, mot_file)
    print(scores)
