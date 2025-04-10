import csv
import numpy as np
import os
import sys

if len(sys.argv) != 3:
    print("Usage: python convertCSV.py <session_id> <trial_name>")
    sys.exit(1)

session_id = sys.argv[1].strip()
trial_name = sys.argv[2].strip()

# Define base data folder where files are downloaded
data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session_id}')

def parse_mot_file(mot_file_path):
    """
    Parse a .mot file and return the data as a list of lists.
    
    :param mot_file_path: Path to the input .mot file
    :return: Parsed data
    """
    data = []
    with open(mot_file_path, 'r') as file:
        lines = file.readlines()
        header_skipped = False
        for line in lines:
            if line.strip() and not header_skipped:
                if line.startswith('time'):
                    header_skipped = True
                continue
            if header_skipped:
                data.append([float(value) for value in line.split()])
    return data

def mot_to_csv(mot_file_path, csv_file_path):
    """
    Convert a .mot file to a .csv file.
    
    :param mot_file_path: Path to the input .mot file
    :param csv_file_path: Path to the output .csv file
    """
    data = parse_mot_file(mot_file_path)
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write header
        csv_writer.writerow([
            'time', 'pelvis_tilt', 'pelvis_list', 'pelvis_rotation', 'pelvis_tx', 'pelvis_ty', 'pelvis_tz',
            'hip_flexion_r', 'hip_adduction_r', 'hip_rotation_r', 'knee_angle_r', 'ankle_angle_r', 'subtalar_angle_r', 'mtp_angle_r',
            'hip_flexion_l', 'hip_adduction_l', 'hip_rotation_l', 'knee_angle_l', 'ankle_angle_l', 'subtalar_angle_l', 'mtp_angle_l',
            'lumbar_extension', 'lumbar_bending', 'lumbar_rotation', 'arm_flex_r', 'arm_add_r', 'arm_rot_r', 'elbow_flex_r', 'pro_sup_r',
            'arm_flex_l', 'arm_add_l', 'arm_rot_l', 'elbow_flex_l', 'pro_sup_l'
        ])
        
        # Write data
        for row in data:
            csv_writer.writerow(row)

# File paths
mot_file_path = os.path.join(data_folder, 'OpenSimData', 'Kinematics', f'{trial_name}.mot')
csv_file_path = mot_file_path.replace('.mot', '.csv')

# Convert .mot to .csv
mot_to_csv(mot_file_path, csv_file_path)