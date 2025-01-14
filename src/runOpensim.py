import sys
import numpy as np
from opensim import *

# Ensure the correct number of arguments are provided
if len(sys.argv) != 4:
    print("Usage: python runOpensim.py <model.osim> <marker_data.trc> <motion.mot>")
    sys.exit(1)

# Get file paths from command-line arguments
model_file = sys.argv[1]
marker_data_file = sys.argv[2]
motion_file = sys.argv[3]

# Function to convert motion file to radians
def convert_motion_file_to_radians(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        header_processed = False

        for line in infile:
            if not header_processed:
                # Write header lines to the output file
                outfile.write(line)
                if line.startswith('inDegrees'):
                    outfile.write('inDegrees=no\n')  # Update inDegrees to "no"
                if line.startswith('endheader'):
                    header_processed = True
            else:
                # Process numeric data lines
                parts = line.split()
                try:
                    # Convert numeric values; skip non-numeric values like column headers
                    data = [float(x) for x in parts]
                    # Convert angular data (e.g., columns > 1) from degrees to radians
                    converted_data = [np.radians(value) if i > 0 else value for i, value in enumerate(data)]
                    outfile.write(' '.join(f"{val:.6f}" for val in converted_data) + '\n')
                except ValueError:
                    # Write the column headers (non-numeric lines) as-is
                    outfile.write(line)

# Convert the motion file to radians
motion_radians_file = motion_file.rsplit('.', 1)[0] + '_radians.mot'
convert_motion_file_to_radians(motion_file, motion_radians_file)

model_file = r'C:\Users\parkj\Downloads\OpenCap\OpenCap\OpenSimData\Model\LaiUhlrich2022_scaled.osim'

# Load the model
model = Model(model_file)
model.setUseVisualizer(True)  # Enable the visualizer

# Initialize the model
state = model.initSystem()

# Load the motion file
motion = Storage(motion_radians_file)

# Convert the motion data to a StatesTrajectory
states_trajectory = StatesTrajectory.createFromStatesStorage(model, motion, True, False)

# Set up the visualizer with a white background
visualizer = model.updVisualizer().updSimbodyVisualizer()

# Set the background color to white
visualizer.setBackgroundColor(Vec3(1.0, 1.0, 1.0))  # RGB for white color
visualizer.setBackgroundType(SimTKVisualizer.SolidColor)  # Use solid color background

# Set real-time simulation speed (1.0 for normal speed)
visualizer.setRealTimeScale(1.0)

# Show simulation time on the visualizer
visualizer.setShowSimTime(True)

# Show frame rate in the visualizer
visualizer.setShowFrameRate(True)

# Enable shadows for better realism
visualizer.setShowShadows(True)

# Enable or disable frame number display (True to show it)
visualizer.setShowFrameNumber(True)

# Visualize the motion
for state in states_trajectory:
    model.getVisualizer().show(state)

# Explicitly delete the state objects after use
del state
