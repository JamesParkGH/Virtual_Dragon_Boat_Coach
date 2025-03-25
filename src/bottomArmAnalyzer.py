import sys
import os
import pandas as pd
import re
import math

from constants import *

def bottomArmAnalyzer(trc_df, mot_df, frame_l, frame_u, stroke_phases, bottom_elbow_x_index, bottom_wrist_x_index):
    angle_count = False
    angle_count_updated = False

    elbow_track_count = 0

    elbow_positions = []
    wrist_positions = []

    for frame in range(frame_l, frame_u):

        # Elbow angle
        if angle_count_updated==False and 180-mot_df['elbow_flex_bottom'].values[frame] < BOTTOM_ELBOW_ANGLE_THRESHOLD:
            angle_count = True
            angle_count_updated = True

        # Elbow tracking out (z position of elbow and wrist)
        if stroke_phases[frame]=='recovery':
            elbow_positions.append(trc_df.iloc[frame, bottom_elbow_x_index+2])
            wrist_positions.append(trc_df.iloc[frame, bottom_wrist_x_index+2])

    if (sum(wrist_positions)/len(wrist_positions))/(sum(elbow_positions)/len(elbow_positions)) > BOTTOM_ELBOW_TRACK_THRESHOLD:
        elbow_track_count += 1


    return angle_count, elbow_track_count