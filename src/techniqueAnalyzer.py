import sys
import os
import pandas as pd
import re
import math
from identifyPaddlingSide import identifyPaddlingSide
from strokeCounter import strokeCounter
from identifyPhase import identifyPhase

def techniqueAnalyzer(trc_file, mot_file):
    try:
        right_side = identifyPaddlingSide(trc_file)

        # put necessary columns into new csv
        df = pd.read_csv(mot_file)
        df = df[['time', 'hip_flexion_r', 'knee_angle_r', 'hip_flexion_l', 'knee_angle_l', 'lumbar_extension', 'lumbar_bending', 'arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l']]

        # reassign left/right to top/bottom accordingly based on right_side
        if right_side:
            df.rename(columns=lambda x: re.sub(r"_r$", "_bottom", x), inplace=True)
            df.rename(columns=lambda x: re.sub(r"_l$", "_top", x), inplace=True)
            
        else:
            df.rename(columns=lambda x: re.sub(r"_l$", "_bottom", x), inplace=True)
            df.rename(columns=lambda x: re.sub(r"_r$", "_top", x), inplace=True)


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
        paddle_angle_ratios = []
        paddle_angle_count = 0  # Added to count instances of bad paddle angle

        curr_stroke = 0
        
        # loop through df
        # Start at first full stroke (stroke_frames[0])
        for frame in range(stroke_frames[0], df.shape[0]):
            # Make sure frame is within stroke_phases range
            if frame >= len(stroke_phases):
                break
                
            # track timeframe of threshold violations (start and stop)
            if frame in stroke_frames:
                # Reset update indicators on each stroke
                top_arm_updated = False
                bottom_elbow_updated = False
                posture_count_updated = False  # Fixed: was posture_count = False

                # Check positive frame ratio
                if frame > stroke_frames[0]:
                    stroke_duration = stroke_frames[curr_stroke] - stroke_frames[curr_stroke-1]

                # if curr_stroke > 0 and positive_frames/(stroke_frames[curr_stroke]-stroke_frames[curr_stroke-1]) < 0:   # UPDATE THRESHOLD
                #     paddle_angle_count += 1
                #     # Keep ratio data
                positive_frames = 0
                # inc stroke count
                curr_stroke += 1

            # Top arm UPPER threshold check (top flex, top add, top rot)
            if top_arm_updated == False and df['arm_flex_top'].values[frame] > 50 and df['arm_add_top'].values[frame] < 170 and df['arm_rot_top'].values[frame] > 160:
                top_arm_count += 1
                top_arm_updated = True

            # Top arm LOWER threshold check (top flex, top add, top rot)

            # Bottom arm UPPER threshold check (bottom elbow)
            if bottom_elbow_updated == False and df['elbow_flex_bottom'].values[frame] < 75:
                bottom_elbow_count += 1
                bottom_elbow_updated = True

            # Bottom arm LOWER threshold check (bottom elbow)

            # Spine posture threshold check (lumbar extension, bending)
            if posture_count_updated == False and df['lumbar_extension'].values[frame] > 240 and df['arm_add_top'].values[frame] < 180:
                posture_count += 1
                posture_count_updated = True

            # Paddle angle threshold check (trc_file: top/bottom wrist x+y components)
            # Duration of angle being positive (time ratio between positive_frames:total_frames)
            try:
                x_diff = top_wrist_x_index.iloc[frame] - bottom_wrist_x_index.iloc[frame]
                y_diff = top_wrist_y_index.iloc[frame] - bottom_wrist_y_index.iloc[frame]
                theta = math.degrees(math.atan(y_diff / x_diff))
                if theta <= 10 and stroke_phases[frame] == "pull":
                    positive_frames += 1
            except Exception as e:
                print(f"Warning: Error calculating paddle angle at frame {frame}: {e}")

        ##############################################################
        # Analysis
        ##############################################################
        if stroke_count > 0:
            top_arm_upper_score = top_arm_count / stroke_count
            # top_arm_lower_score = 0
            bottom_elbow_upper_score = bottom_elbow_count / stroke_count
            # bottom_elbow_lower_score = 0
            posture_score = posture_count / stroke_count
             
            # FIXED: Use sum() function with paddle_angle_ratios
            if paddle_angle_ratios:  # Check if we have any ratios
                paddle_angle_score = sum(paddle_angle_ratios) / len(paddle_angle_ratios)
            else:
                paddle_angle_score = 0
        else:
            top_arm_upper_score = bottom_elbow_upper_score = posture_score = paddle_angle_score = 0

        # Debug output
        print("Paddle angle ratios:", paddle_angle_ratios)
        print(f"Scores: {top_arm_upper_score}, {bottom_elbow_upper_score}, {posture_score}, {paddle_angle_score}")
        
        return [top_arm_upper_score, bottom_elbow_upper_score, posture_score, paddle_angle_score]
        
    except Exception as e:
        print(f"Error in techniqueAnalyzer: {e}")
        import traceback
        traceback.print_exc()
        return [0, 0, 0, 0]  # Return zeros in case of error

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python techniqueAnalyzer.py <trc_file> <mot_file>")
        sys.exit(1)

    trc_file = sys.argv[1]
    mot_file = sys.argv[2]

    scores = techniqueAnalyzer(trc_file, mot_file)
    print(scores)