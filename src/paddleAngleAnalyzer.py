import sys
import os
import pandas as pd
import re
import math

from constants import *

def paddleAngleAnalyzer(trc_df, mot_df, stroke_phases, bottom_wrist_x_index, top_wrist_x_index):

    pull_frames = 0
    positive_frames = 0

    for frame in range(trc_df.shape[0]):

        x_diff = (float(trc_df.iloc[frame,top_wrist_x_index] - trc_df.iloc[frame,bottom_wrist_x_index]))
        y_diff = (float(trc_df.iloc[frame,top_wrist_x_index+1] - trc_df.iloc[frame,bottom_wrist_x_index+1]))

        theta = math.degrees(math.atan(y_diff/x_diff))
        if stroke_phases[frame]=="pull":
            pull_frames += 1
            if theta <= 10:
                positive_frames += 1

    positive_ratio = positive_frames/pull_frames
    
    return positive_ratio