import sys
import pandas as pd

if len(sys.argv) != 3:
    print("Usage: python techniqueAnalyzer.py <session_id> <trial_name>")
    sys.exit(1)

session_id = sys.argv[1]
trial_name = sys.argv[2]

# Define the path to the CSV file
csv_file = f"Data/OpenCapData_{session_id}/OpenSimData/Kinematics/{trial_name}.csv"

# Read the CSV file
data = pd.read_csv(csv_file)

# Extract the elbow flexion data for the right arm and adjust the angle
elbow_flex_r = 180 - data['elbow_flex_r']

# Calculate the lowest and highest values
lowest_value = elbow_flex_r.min()
highest_value = elbow_flex_r.max()

# Check if the values are within the acceptable range
if lowest_value < 130 or highest_value > 160:
    image_filename = "flagBottomArm.png"
else:
    image_filename = "goodBottomArm.png"

# Print the image filename to stdout
print(image_filename)