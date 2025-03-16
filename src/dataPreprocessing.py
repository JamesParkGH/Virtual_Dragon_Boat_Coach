import sys
import os
import pandas as pd
import re
from identifyPaddlingSide import identifyPaddlingSide

def dataPreprocessing(trc, mot):
    right_side = identifyPaddlingSide(trc)

    # put necessary columns into new csv
    mot_df = pd.read_csv(mot)
    mot_df = mot_df[['time', 'hip_flexion_r', 'knee_angle_r', 'hip_flexion_l', 'knee_angle_l', 'lumbar_extension', 'lumbar_bending', 'arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l']]

    trc_df = pd.read_csv(trc, sep=",", engine="python", header=None)

    neck_x_index = trc_df.iloc[:,2]
    

    # reassign left/right to top/bottom accordingly based on right_side
    if right_side:
        mot_df.rename(columns=lambda x: re.sub(r"[_r]{2}$", "_bottom", x), inplace=True)
        mot_df.rename(columns=lambda x: re.sub(r"[_l]{2}$", "_top", x), inplace=True)
        
        bottom_wrist_x_index = 11    # right side   
        bottom_shoulder_x_index = 5
        bottom_elbow_x_index = 8
        bottom_hip_x_index = 26
        bottom_knee_x_index = 29

        top_wrist_x_index = 20
        top_shoulder_x_index = 14
        top_elbow_x_index = 17
        top_hip_x_index = 35
        top_knee_x_index = 38

    else:
        mot_df.rename(columns=lambda x: re.sub(r"[_l]{2}$", "_bottom", x), inplace=True)
        mot_df.rename(columns=lambda x: re.sub(r"[_r]{2}$", "_top", x), inplace=True)

        top_wrist_x_index = 11    # left side   
        top_shoulder_x_index = 5
        top_elbow_x_index = 8
        top_hip_x_index = 26
        top_knee_x_index = 29

        bottom_wrist_x_index = 20
        bottom_shoulder_x_index = 14
        bottom_elbow_x_index = 17
        bottom_hip_x_index = 35
        bottom_knee_x_index = 38



    return mot_df, neck_x_index, top_wrist_x_index, top_shoulder_x_index, top_elbow_x_index, top_hip_x_index, top_knee_x_index, bottom_wrist_x_index, bottom_shoulder_x_index, bottom_elbow_x_index, bottom_hip_x_index, bottom_knee_x_index