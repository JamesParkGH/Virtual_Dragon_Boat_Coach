import csv
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd

def identifyPaddlingSide(trc_file_path, mot_file_path):
    right_side = True

    time = []
    angle_data = []

    # Read through .trc to find which side is the top vs bottom (get avg y_value)
    df = pd.read_csv("paddling1_trc.csv", sep=",", engine="python", header=None, index_col=0)

    right_wrist = df.iloc[:,11]

    print(right_wrist)

        
    

    # with open(mot_file_path, 'r') as mot_file:
    #     csv_reader = csv.DictReader(mot_file)
    #     for row in csv_reader:
    #         time.append(float(row['time']))
    #         angle_data.append(180 - float(row[angle]))


    # Ensure output directory exists
    # os.makedirs(output_dir, exist_ok=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python plotAngle.py <session_id> <trial_name> <angle_name>")
        sys.exit(1)

    # session_id = sys.argv[1].strip()
    # trial_name = sys.argv[2].strip()
    # angle_name = sys.argv[3].strip()

    # Define the path to the CSV file and output directory
    # kinematics_dir = os.path.join('Data', f'OpenCapData_{session_id}', 'OpenSimData', 'Kinematics')
    # csv_file_path = os.path.join(kinematics_dir, f'{trial_name}.csv')

    # Ensure the CSV file exists
    # if not os.path.exists(csv_file_path):
    #     print(f"Error: CSV file not found: {csv_file_path}")
    #     sys.exit(1)

    # Plot the specified angle and save the plot
    identifyPaddlingSide("paddling1_trc.csv", "paddling1_trc.csv")
