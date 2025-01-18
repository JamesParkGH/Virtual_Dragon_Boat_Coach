import csv

file_path = r"D:\McMaster\Year 5\5P06A\data\2025-01-13 Session\MarkerData\IainDBAC1.csv"

with open(file_path, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

#Extract metadata, headers, sub-headers and data
metadata = rows[:3]
headers = rows[3]
print(headers)
sub_headers = rows[4]
data = rows[6:]

#Identify indices
RWrist_x_index = headers.index("RWrist")
RWrist_y_index = headers.index("RWrist") + 1
RWrist_z_index = headers.index("RWrist") + 2

phase = "None"

for i in range(len(data)-1):
    if float(data[i][RWrist_x_index]) - float(data[i+1][RWrist_x_index]) > 0.015:
        if phase != "pull":
            phase = "pull"
            print("phase changed to pull at: ", data[i][1], " second")
            print(data[i][RWrist_x_index])
            print(data[i+1][RWrist_x_index])
    elif abs(float(data[i][RWrist_x_index]) - float(data[i+1][RWrist_x_index])) > 0.015:
        if phase != "relax":
            phase = "relax"
            print("phase changed to relax at: ", data[i][1], " second")
    else:
        pass
    data[i].append(phase)

headers.append("")
headers.append("")
headers.append("Phase")

output_file = "phased_data.csv"
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(metadata)
    writer.writerow(headers)
    writer.writerow(sub_headers)
    writer.writerows(data)
    
