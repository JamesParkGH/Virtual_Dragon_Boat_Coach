import csv
import matplotlib.pyplot as plt

def plot_angle(csv_file_path, angle):
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
    plt.show()

def get_available_angles(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
    return header[1:]  # Exclude 'time' from the list

# File path
csv_file_path = r"C:\Users\richa\OneDrive\Desktop\FinalYear\Fall\5P06\github\Virtual_Dragon_Boat_Coach\src\Data\OpenCapData_4c352cef-dc9b-4f3b-92ec-70846d8633cc\OpenSimData\Kinematics\IainDBAC1.csv"

# Get the list of available angles
available_angles = get_available_angles(csv_file_path)

# Display the available angles to the user
print("Available angles to plot:")
for angle in available_angles:
    print(angle)

# Ask the user for the angle to plot
angle = input("Enter the angle you want to plot: ")

# Plot the specified angle
plot_angle(csv_file_path, angle)