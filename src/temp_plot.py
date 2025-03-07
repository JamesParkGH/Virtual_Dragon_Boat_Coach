import csv
import matplotlib.pyplot as plt
import sys
import os

def plot_angle(csv_file_path):
    time = []
    angle1_data = []
    angle2_data = []

    angle1 = 'arm_rot_l'
    angle2 = 'elbow_flex_l'

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            time.append(float(row['time']))
            angle1_data.append(180 - float(row[angle1]))
            angle2_data.append(180 - float(row[angle2]))


    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(time, angle1_data, label=angle1)
    ax1.set_title(f'{angle1} vs Time')
    ax2.plot(time, angle2_data, label=angle2)
    ax2.set_title(f'{angle2} vs Time')
    

    # Show the plot
    plt.show()

plot_angle("Ed_paddling_mot.csv")