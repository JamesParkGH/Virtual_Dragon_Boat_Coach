import csv
import pandas as pd
from identifyPaddlingSide import identifyPaddlingSide

def strokeCounter(trc_file_path):
    df = pd.read_csv(trc_file_path, sep=",", engine="python", header=None)

    #Identify indices (y and z not used for now)
    if identifyPaddlingSide(trc_file_path):
        bottom_wrist_x_index = df.iloc[:,11]    #right wrist
    else:
        bottom_wrist_x_index = df.iloc[:,20]    #left wrist

    right_ankle_x_index = df.iloc[:,32]
    Time_index = df.iloc[:,0]

    stroke_time_stamp = []
    stroke_number = 0
    stroke_interval = 0
    stroke_counted = False

    for i in range(len(df)-4):
        pulling = bottom_wrist_x_index.iloc[i] > bottom_wrist_x_index.iloc[i+1] and bottom_wrist_x_index.iloc[i+1] > bottom_wrist_x_index.iloc[i+2] and bottom_wrist_x_index.iloc[i+2] > bottom_wrist_x_index.iloc[i+3]
        starting = float(bottom_wrist_x_index.iloc[i]) > float(right_ankle_x_index.iloc[i])

        if pulling and starting and not stroke_counted:
            stroke_counted = True
            stroke_number += 1
            stroke_time_stamp.append(Time_index.iloc[i])
            stroke_interval = 40
            # print("marking stroke ", stroke_number, " at time: ", Time_index.iloc[i], " seconds")
        elif stroke_interval > 0:
            stroke_interval -= 1
            if stroke_interval == 0:
                stroke_counted = False
        else:
            pass
    
    # print(stroke_number, stroke_time_stamp)
    return stroke_number, stroke_time_stamp

strokeCounter("Frank_paddling_trc.csv")