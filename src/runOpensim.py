import os
import sys
import numpy as np
from opensim import *

# Ensure the correct number of arguments are provided
if len(sys.argv) != 3:
    print("Usage: python runOpensim.py <session_id> <trial_name>")
    sys.exit(1)

# Get session ID and trial name from command-line arguments
session_id = sys.argv[1].strip()
trial_name = sys.argv[2].strip()

# Define base data folder where files are downloaded
data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session_id}')

# Define file paths dynamically using the trial name
#model_file = r'C:\Users\parkj\Downloads\OpenCap\OpenCap\OpenSimData\Model\LaiUhlrich2022_scaled.osim'
model_file = os.path.join(os.getcwd(), 'Data', 'LaiUhlrich2022_scaled.osim')
marker_data_file = os.path.join(data_folder, 'MarkerData', f'{trial_name}.trc')  # Use trial name here
motion_file = os.path.join(data_folder, 'OpenSimData', 'Kinematics', f'{trial_name}.mot')  # Use trial name here

# Ensure required files exist before proceeding
for file in [marker_data_file, motion_file]:
    if not os.path.isfile(file):
        print(f"Error: Required file not found: {file}")
        sys.exit(1)

# Function to convert motion file to radians
def convert_motion_file_to_radians(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        header_processed = False

        for line in infile:
            if not header_processed:
                outfile.write(line)
                if line.startswith('inDegrees'):
                    outfile.write('inDegrees=no\n')  # Update inDegrees to "no"
                if line.startswith('endheader'):
                    header_processed = True
            else:
                parts = line.split()
                try:
                    data = [float(x) for x in parts]
                    converted_data = [np.radians(value) if i > 0 else value for i, value in enumerate(data)]
                    outfile.write(' '.join(f"{val:.6f}" for val in converted_data) + '\n')
                except ValueError:
                    outfile.write(line)

# Convert motion file to radians
motion_radians_file = motion_file.rsplit('.', 1)[0] + '_radians.mot'
convert_motion_file_to_radians(motion_file, motion_radians_file)

# Load the model
model = Model(model_file)
model.setUseVisualizer(True)

# Initialize the model
state = model.initSystem()

# Load the motion file
motion = Storage(motion_radians_file)

# Convert the motion data to a StatesTrajectory
states_trajectory = StatesTrajectory.createFromStatesStorage(model, motion, True, False)

# Set up the visualizer
visualizer = model.updVisualizer().updSimbodyVisualizer()
visualizer.setBackgroundColor(Vec3(1.0, 1.0, 1.0))  # White background
visualizer.setBackgroundType(SimTKVisualizer.SolidColor)
visualizer.setRealTimeScale(1.0)
visualizer.setShowSimTime(True)
visualizer.setShowFrameRate(True)
visualizer.setShowShadows(True)
visualizer.setShowFrameNumber(True)

# Visualize the motion
for state in states_trajectory:
    model.getVisualizer().show(state)

# Explicitly delete the state object
del state