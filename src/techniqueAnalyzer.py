import sys
import os
import pandas as pd
import re
import math
from identifyPaddlingSide import identifyPaddlingSide
from strokeCounter import strokeCounter

def techniqueAnalyzer(trc_file, mot_file):
    right_side = identifyPaddlingSide(trc_file)

    # put necessary columns into new csv
    df = pd.read_csv(mot_file)
    df = df[['time', 'hip_flexion_r', 'knee_angle_r', 'hip_flexion_l', 'knee_angle_l', 'lumbar_extension', 'lumbar_bending', 'arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l']]

    # reassign left/right to top/bottom accordingly based on right_side
    if right_side:
        df.rename(columns=lambda x: re.sub(r"[_r]{2}$", "_bottom", x), inplace=True)
        df.rename(columns=lambda x: re.sub(r"[_l]{2}$", "_top", x), inplace=True)
        
    else:
        df.rename(columns=lambda x: re.sub(r"[_l]{2}$", "_bottom", x), inplace=True)
        df.rename(columns=lambda x: re.sub(r"[_r]{2}$", "_top", x), inplace=True)


    # track number of threshold violations
    # need to make sure not over counting -> only increment by 1 per cycle
    # need elapsed number of strokes
    stroke_count, stroke_frames = strokeCounter(trc_file)
    stroke_count -= 1   # Gives intervals instead of end markers

    # Cannot exceed curr_stroke
    top_arm_count = 0
    top_arm_updated = False

    bottom_elbow_count = 0
    bottom_elbow_updated = False

    posture_count = 0
    posture_count_updated = False


    # Paddle angle
    trc_df = pd.read_csv(trc_file, sep=",", engine="python", header=None)

    #Identify indices (y and z not used for now)
    if right_side:
        bottom_wrist_x_index = trc_df.iloc[:,11]    #right side
        bottom_wrist_y_index = trc_df.iloc[:,12]    
        top_wrist_x_index = trc_df.iloc[:,20]
        top_wrist_y_index = trc_df.iloc[:,21]
    else:
        bottom_wrist_x_index = trc_df.iloc[:,20]    #left side
        bottom_wrist_y_index = trc_df.iloc[:,21]
        top_wrist_x_index = trc_df.iloc[:,11]
        top_wrist_y_index = trc_df.iloc[:,12]

    positive_frames = 0
    paddle_angle_count = 0


    curr_stroke = 0
    
    # loop through df
    # Start at first full stroke (stroke_frames[0])
    for frame in range(stroke_frames[0], df.shape[0]):

    # track timeframe of threshold violations (start and stop)
        if frame in stroke_frames:

            # Reset update indicators on each stroke
            top_arm_updated = False
            bottom_elbow_updated = False
            posture_count = False

            # Check positive frame ratio
            if curr_stroke > 0 and positive_frames/(stroke_frames[curr_stroke]-stroke_frames[curr_stroke-1]) < 0:   # UPDATE THRESHOLD
                paddle_angle_count += 1
                # Keep ratio data
            positive_frames = 0

            # inc stroke count
            curr_stroke += 1


    # Top arm UPPER threshold check (top flex, top add, top rot)
        if top_arm_updated==False and df['arm_flex_top'].values[frame] > 0 and df['arm_add_top'].values[frame] > 0 and df['arm_rot_top'].values[frame] > 0:
            top_arm_count += 1
            top_arm_updated = True

    # Top arm LOWER threshold check (top flex, top add, top rot)

    # Bottom arm UPPER threshold check (bottom elbow)
        if bottom_elbow_updated==False and df['elbow_flex_bottom'].values[frame] > 0:
            bottom_elbow_count += 1

    # Bottom arm LOWER threshold check (bottom elbow)


    # Spine posture threshold check (lumbar extension, bending)

    # Paddle angle threshold check (trc_file: top/bottom wrist x+y components)
    # Duration of angle being positive (time ratio between positive_frames:total_frames)
        x_diff = top_wrist_x_index.iloc[frame] - bottom_wrist_x_index.iloc[frame]
        y_diff = top_wrist_y_index.iloc[frame] - bottom_wrist_y_index.iloc[frame]
        theta = math.atan(y_diff/x_diff)
        if theta <= math.pi/2:
            positive_frames += 1

    ##############################################################
    # Analysis
    ##############################################################
    top_arm_upper_score = top_arm_count/stroke_count
    top_arm_lower_score = 0
    bottom_elbow_upper_score = bottom_elbow_count/stroke_count
    bottom_elbow_lower_score = 0
    posture_score = 0
    paddle_angle_score = paddle_angle_count/stroke_count

    return [top_arm_upper_score, top_arm_lower_score, bottom_elbow_upper_score, bottom_elbow_lower_score, posture_score, paddle_angle_score]

mot_file = "Frank_paddling_mot.csv"
trc_file = "Frank_paddling_trc.csv"

techniqueAnalyzer(trc_file, mot_file)