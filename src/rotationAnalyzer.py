import sys
import os
import pandas as pd
import re
import math

from constants import *

def rotationAnalyzer(trc_df, mot_df, frame_l, frame_u, bottom_shoulder_x_index, top_shoulder_x_index):
    # Calculate shoulder width
    x_diff = (abs(float(trc_df.iloc[1,bottom_shoulder_x_index] - trc_df.iloc[1,top_shoulder_x_index])))
    y_diff = (abs(float(trc_df.iloc[1,bottom_shoulder_x_index+1] - trc_df.iloc[1,top_shoulder_x_index+1])))
    z_diff = (abs(float(trc_df.iloc[1,bottom_shoulder_x_index+2] - trc_df.iloc[1,top_shoulder_x_index+2])))

    shoulder_width = math.sqrt(x_diff**2 + y_diff**2 + z_diff**2)
    
    front_rotation_count = 1
    front_count_updated = False

    back_rotation_count = 0
    back_count_updated = False


    for frame in range(frame_l, frame_u):
        x_val = (float(trc_df.iloc[frame,bottom_shoulder_x_index] - trc_df.iloc[frame,top_shoulder_x_index]))/shoulder_width
        y_val = 0
        z_val = 0
        if not front_count_updated and not back_count_updated:
            if x_val > 0.25:
                front_rotation_count -= 1
                front_count_updated = True
            if x_val < -0.4:
                back_rotation_count += 1
                back_count_updated = True
        else:
            break

    
    return front_rotation_count, back_rotation_count