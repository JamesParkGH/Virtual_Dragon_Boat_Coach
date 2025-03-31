import sys
import os
import pandas as pd
import re
import math

from constants import *

def paddleAngleAnalyzer(trc_df, mot_df, frame_l, frame_u, stroke_phases, bottom_wrist_x_index, top_wrist_x_index):

    pull_frames = 0
    positive_frames = 0

    negative_count = 0
    negative_count_updated = False

    for frame in range(frame_l, frame_u):

        x_diff = (float(trc_df.iloc[frame,top_wrist_x_index] - trc_df.iloc[frame,bottom_wrist_x_index]))
        y_diff = (float(trc_df.iloc[frame,top_wrist_x_index+1] - trc_df.iloc[frame,bottom_wrist_x_index+1]))

        theta = math.degrees(math.atan(y_diff/x_diff))
        if stroke_phases[frame]=="pull":
            pull_frames += 1
            if theta <= 10:
                positive_frames += 1
            if negative_count_updated==False and mot_df['hip_flexion_bottom'].values[frame] < 80 and theta > 30:
                negative_count += 1
                negative_count_updated = True

    positive_ratio = positive_frames/pull_frames
    
    return positive_ratio, negative_count