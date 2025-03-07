import csv
import pandas as pd
from identifyPaddlingSide import identifyPaddlingSide

def identifyPhase(trc_file_path):
    df = pd.read_csv(trc_file_path, sep=",", engine="python", header=None)

    #Identify indices (y and z not used for now)
    if identifyPaddlingSide(trc_file_path):
        bottom_wrist_x_index = df.iloc[:,11]    #right wrist
    else:
        bottom_wrist_x_index = df.iloc[:,20]    #left wrist


    phase = "None"
    phase_list = []

    for i in range(1,df.shape[0]):
        #Compare the x value between the data points
        if float(bottom_wrist_x_index[i-1]) - float(bottom_wrist_x_index[i]) > 0.015:
            if phase != "pull":
                phase = "pull"
        elif abs(float(bottom_wrist_x_index[i-1]) - float(bottom_wrist_x_index[i])) > 0.015:
            if phase != "recovery":
                phase = "recovery"
        else:
            pass
        if len(phase_list)==0:
            phase_list.append(phase)
        phase_list.append(phase)

    return phase_list
