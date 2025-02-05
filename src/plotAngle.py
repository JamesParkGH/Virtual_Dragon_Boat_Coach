import csv
import matplotlib.pyplot as plt
import sys
import os

def plot_angle(csv_file_path, angle, output_dir):
    time = []
    angle_data = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            time.append(float(row['time']))
            angle_data.append(float(row[angle]))

    plt.figure()
    plt.plot(time, angle_data, label=angle)
    plt.xlabel('Time (s)')
    plt.ylabel(f'{angle} (degrees)')
    plt.title(f'{angle} vs Time')
    plt.legend()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot
    plot_filename = os.path.join(output_dir, f'{angle}_plot.png')
    plt.savefig(plot_filename)

    # Show the plot
    plt.show()

    print(f"Plot saved to: {plot_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python plotAngle.py <session_id> <trial_name> <angle_name>")
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

    # Plot the specified angle and save the plot
    plot_angle(csv_file_path, angle_name, kinematics_dir)
