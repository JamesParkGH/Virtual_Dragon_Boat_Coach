import sys
import os
import pandas as pd
import re
import math
import numpy as np

from constants import *

def topArmAnalyzer(trc_df, mot_df, frame_l, frame_u, stroke_phases, top_wrist_x_index, top_shoulder_x_index, top_elbow_x_index):
    wrist_shoulder_diff = []

    wrist_velocity = []
    elbow_velocity = []
    
    elbow_count = 0
    elbow_count_updated = False

    wrist_shoulder_count = 0

    elbow_hammer_count = 1

    pull_frames = [0,0]
    prev_phase = "recovery"

    for frame in range(frame_l, frame_u):
        # Elbow angle
        if elbow_count_updated==False and stroke_phases[frame]=='recovery' and 180-mot_df['arm_flex_top'].values[frame] > TOP_ARM_FLEX_THRESHOLD and 180-mot_df['arm_add_top'].values[frame] < TOP_ARM_ADD_THRESHOLD and 180-mot_df['arm_rot_top'].values[frame] > TOP_ARM_ROT_THRESHOLD and 180-mot_df['elbow_flex_top'].values[frame] < TOP_ELBOW_THRESHOLD:
            elbow_count += 1
            elbow_count_updated = True

        # Top wrist/shoulder ratio (NEEDS TO BE DIVIDED BY MAX VAL)
        wrist_shoulder_diff.append(abs(float(trc_df.iloc[frame,top_wrist_x_index] - trc_df.iloc[frame,top_shoulder_x_index])))

        # Identify first and last pull frames
        if stroke_phases[frame]=="pull" and pull_frames[0]==0:
            if prev_phase != "pull" or frame==frame_l:
                pull_frames[0] = frame
        if stroke_phases[frame]!="pull" and prev_phase == "pull":
                pull_frames[1] = frame

        prev_phase = stroke_phases[frame]

    # Normalize wrist-shoulder distnces
    max_diff = max(wrist_shoulder_diff)
    wrist_shoulder_diff_norm = [x/max_diff for x in wrist_shoulder_diff]
    wrist_shoulder_count = not all(x > TOP_HAND_MOVEMENT_RATIO_THRESHOLD for x in wrist_shoulder_diff_norm)
    
    # Derivative of wrist and elbow y-position (trc file)

    wrist_velocity = np.gradient(trc_df.iloc[pull_frames[0]:pull_frames[1], top_wrist_x_index+1], trc_df.iloc[pull_frames[0]:pull_frames[1],1])
    elbow_velocity = np.gradient(trc_df.iloc[pull_frames[0]:pull_frames[1], top_elbow_x_index+1], trc_df.iloc[pull_frames[0]:pull_frames[1],1])

    velocity_ratio = [elbow/wrist for elbow, wrist in zip(elbow_velocity, wrist_velocity)]

    if max(velocity_ratio) < ELBOW_VELOCITY_RATIO_THRESHOLD:
        elbow_hammer_count -= 1

    return elbow_count, wrist_shoulder_count, elbow_hammer_count