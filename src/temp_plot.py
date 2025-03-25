import csv
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
from statistics import variance
import math

def plot_angle(trc_file, mot_file):
    time = []
    angle1_data = []
    angle2_data = []

    trc_point1_data = []
    trc_point2_data = []
    trc_point3_data = []
    length = []

    angle1 = 'hip_flexion_r'
    angle2 = 'knee_angle_r'
    

    trc_df = pd.read_csv(trc_file , sep=",", engine="python", header=None)

    with open(mot_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            time.append(float(row['time']))
            angle1_data.append(float(row[angle1]))
            angle2_data.append(float(row[angle2]))
        for i in range(trc_df.shape[0]):
            trc_point1_data.append((float(trc_df.iloc[i,2] - trc_df.iloc[i,23])))
            trc_point2_data.append((float(trc_df.iloc[i,3] - trc_df.iloc[i,24])))
            trc_point3_data.append((float(trc_df.iloc[i,4] - trc_df.iloc[i,25])))

            x_diff = abs((float(trc_df.iloc[i,2] - trc_df.iloc[i,23])))
            y_diff = abs((float(trc_df.iloc[i,3] - trc_df.iloc[i,24])))
            z_diff = abs((float(trc_df.iloc[i,4] - trc_df.iloc[i,25])))
            length.append(math.sqrt(x_diff**2 + y_diff**2 + z_diff**2))

    x_diff = abs((float(trc_df.iloc[1,2] - trc_df.iloc[1,23])))
    y_diff = abs((float(trc_df.iloc[1,3] - trc_df.iloc[1,24])))
    z_diff = abs((float(trc_df.iloc[1,4] - trc_df.iloc[1,25])))

    shoulder_width = math.sqrt(x_diff**2 + y_diff**2 + z_diff**2)

    # max_x = max(trc_point1_data)
    # max_y = max(trc_point2_data)
    # max_z = max(trc_point3_data)

    trc_point1_data = [x/shoulder_width for x in trc_point1_data]
    trc_point2_data = [x/shoulder_width for x in trc_point2_data]
    trc_point3_data = [x/shoulder_width for x in trc_point3_data]

    print(sum(trc_point1_data)/len(trc_point1_data))
    print(sum(trc_point2_data)/len(trc_point2_data))
    print(sum(trc_point3_data)/len(trc_point2_data))

    # print(variance(trc_point1_data))
    # print(variance(trc_point2_data))
    # print(variance(trc_point3_data))

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(time, angle1_data, label=angle1)
    ax1.set_title(f'{angle1} vs Time')
    ax2.plot(time, angle2_data, label=angle2)
    ax2.set_title(f'{angle2} vs Time')


    # fig, (ax1, ax2, ax3) = plt.subplots(1,3)
    # ax1.plot(time, trc_point1_data)
    # ax1.set_title('Shoulder_x vs Time')
    # ax2.plot(time, trc_point2_data)
    # ax2.set_title('Shoulder_y vs Time')
    # ax3.plot(time, trc_point3_data)
    # ax3.set_title('Shoulder_z vs Time')
    
    # fig, ax = plt.subplots(1,1)
    # ax.plot(time, length)
    # ax.set_title('Spine Length vs Time')

    # Show the plot
    plt.show()

# plot_angle("IainDBAC1_trc.csv", "IainDBAC1_mot.csv")
plot_angle("Richard_AB1_trc.csv", "Richard_AB1_mot.csv")
# plot_angle("Frank_paddling_trc.csv", "Frank_paddling_mot.csv")
# plot_angle("James_1_trc.csv", "James_1_mot.csv")
# plot_angle("Ed_paddling_trc.csv", "Ed_paddling_mot.csv")