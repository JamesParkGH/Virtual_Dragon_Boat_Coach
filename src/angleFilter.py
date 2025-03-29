import csv
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

def plot_angle(csv_file_path, angle):
    """
    Plot the specified angle from the CSV file.
    
    :param csv_file_path: Path to the input .csv file
    :param angle: The angle to plot
    """
    time = []
    angle_data = []
    
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            time.append(float(row['time']))
            angle_data.append(float(row[angle]))
    
    # Apply Gaussian filter to smooth the data
    smoothed_angle_data = gaussian_filter1d(angle_data, sigma=2)
    
    plt.figure()
    plt.plot(time, angle_data, label=f'{angle} (raw)', color='blue')
    plt.plot(time, smoothed_angle_data, label=f'{angle} (smoothed)', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel(f'{angle} (degrees)')
    plt.title(f'{angle} vs Time')
    plt.legend()
    plt.show()

def get_available_angles(csv_file_path):
    """
    Get the list of available angles from the CSV file header.
    
    :param csv_file_path: Path to the input .csv file
    :return: List of available angles
    """
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
    return header[1:]  # Exclude 'time' from the list


# File path
#import os
#csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\src\\Data\\OpenCapData_4c352cef-dc9b-4f3b-92ec-70846d8633cc\\MarkerData\\IainDBAC1.csv"))

# Get the list of available angles
#available_angles = get_available_angles(csv_file_path)

# Display the available angles to the user
#print("Available angles to plot:")
#for angle in available_angles:
    #print(angle)

# Ask the user for the angle to plot
#angle = input("Enter the angle you want to plot: ")

# Plot the specified angle
#plot_angle(csv_file_path, angle)

