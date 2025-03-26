import csv
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Dictionary mapping angle values to display names
ANGLE_DISPLAY_NAMES = {
    "pelvis_tilt": "Pelvis Tilt",
    "pelvis_list": "Pelvis List",
    "pelvis_rotation": "Pelvis Rotation",
    "pelvis_tx": "Pelvis TX",
    "pelvis_ty": "Pelvis TY",
    "pelvis_tz": "Pelvis TZ",
    "hip_flexion_r": "Right Hip Flexion",
    "hip_adduction_r": "Right Hip Adduction",
    "hip_rotation_r": "Right Hip Rotation",
    "knee_angle_r": "Right Knee Angle",
    "ankle_angle_r": "Right Ankle Angle",
    "subtalar_angle_r": "Right Subtalar Angle",
    "mtp_angle_r": "Right MTP Angle",
    "arm_flex_r": "Right Arm Flexion",
    "arm_add_r": "Right Arm Adduction",
    "arm_rot_r": "Right Arm Rotation",
    "elbow_flex_r": "Right Elbow Flexion",
    "pro_sup_r": "Right Pro Sup",
    "hip_flexion_l": "Left Hip Flexion",
    "hip_adduction_l": "Left Hip Adduction",
    "hip_rotation_l": "Left Hip Rotation",
    "knee_angle_l": "Left Knee Angle",
    "ankle_angle_l": "Left Ankle Angle",
    "subtalar_angle_l": "Left Subtalar Angle",
    "mtp_angle_l": "Left MTP Angle",
    "arm_flex_l": "Left Arm Flexion",
    "arm_add_l": "Left Arm Addion",
    "arm_rot_l": "Left Arm Rotation",
    "elbow_flex_l": "Left Elbow Flexion",
    "pro_sup_l": "Left Pro Sup",
    "lumbar_extension": "Lumbar Extension",
    "lumbar_bending": "Lumbar Bending",
    "lumbar_rotation": "Lumbar Rotation"
}

def load_angle_data(csv_file_path, angle_name):
    time = []
    angle_data = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            try:
                time.append(float(row['time']))
                angle_data.append(180 - float(row[angle_name]))
            except (KeyError, ValueError) as e:
                print(f"Error processing row: {e}")
                continue

    return np.array(time), np.array(angle_data)

def filter_angle_data(angle_data, sigma=2):
    return gaussian_filter1d(angle_data, sigma=sigma)

def get_available_angles(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        headers = csv_reader.fieldnames
        angles = [h for h in headers if h != 'time']
        return angles

def plot_filtered_angle(csv_file_path, angle, session_id, trial_name, sigma=2):
    # Load and filter data
    time, angle_data = load_angle_data(csv_file_path, angle)
    filtered_data = filter_angle_data(angle_data, sigma)
    
    # Get the display name for the angle
    display_name = ANGLE_DISPLAY_NAMES.get(angle, angle)
    
    # Create plot
    plt.figure(figsize=(10, 6))
    # Only plot the filtered data
    plt.plot(time, filtered_data, label=display_name, linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel(f'{display_name} (degrees)')
    plt.title(f'The {display_name} vs Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save to static folder for web access
    static_dir = os.path.join(os.getcwd(), 'static', 'graphs')
    os.makedirs(static_dir, exist_ok=True)
    
    # Save with standard naming convention
    plot_filename = os.path.join(static_dir, f'{trial_name}_{angle}_plot.png')
    plt.savefig(plot_filename)
    plt.close()  # Close the figure to free memory
    
    print(f"Plot saved to: {plot_filename}")
    
    data_folder = os.path.join('Data', f'OpenCapData_{session_id}', 'OpenSimData', 'Kinematics')
    os.makedirs(data_folder, exist_ok=True)
    data_plot_filename = os.path.join(data_folder, f'{trial_name}_{angle}_plot.png')
    plt.figure(figsize=(10, 6))
    plt.plot(time, filtered_data, label=display_name, linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel(f'{display_name} (degrees)')
    plt.title(f'The {display_name} vs Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(data_plot_filename)
    plt.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python plotFilteredAngle.py <session_id> <trial_name> <angle_name>")
        sys.exit(1)

    session_id = sys.argv[1].strip()
    trial_name = sys.argv[2].strip()
    angle_name = sys.argv[3].strip()

    # Define the path to the CSV file and output directory
    kinematics_dir = os.path.join('Data', f'OpenCapData_{session_id}', 'OpenSimData', 'Kinematics')
    csv_file_path = os.path.join(kinematics_dir, f'{trial_name}.csv')

    # Ensure the CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found: {csv_file_path}")
        sys.exit(1)
        
    # If angle_name is "list", show available angles
    if angle_name.lower() == "list":
        available_angles = get_available_angles(csv_file_path)
        print("Available angles to plot:")
        for angle in available_angles:
            display_name = ANGLE_DISPLAY_NAMES.get(angle, angle)
            print(f"{angle}: {display_name}")
        sys.exit(0)

    # Plot the specified angle with filtering and save the plot
    plot_filtered_angle(csv_file_path, angle_name, session_id, trial_name)