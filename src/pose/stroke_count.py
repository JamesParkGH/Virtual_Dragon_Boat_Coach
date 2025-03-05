import csv

def stroke_count(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    #Extract metadata, headers, sub-headers and data
    metadata = rows[:3]
    headers = rows[3]
    sub_headers = rows[4]
    data = rows[6:]

    #Identify indices (y and z not used for now)
    RWrist_x_index = headers.index("RWrist")
    RWrist_y_index = headers.index("RWrist") + 1
    RWrist_z_index = headers.index("RWrist") + 2
    RHeel_x_index = headers.index("RAnkle")

    stroke_time_stamp = {}
    print(data)

    for i in range(len(data)):
        #Compare the x value between the data points
        starting_stroke = data[i][RWrist_x_index] > data[i+1][RWrist_x_index] and data[i+1][RWrist_x_index] > data[i+2][RWrist_x_index] and data[i+2][RWrist_x_index] > data[i+3][RWrist_x_index]
        if () > 0.015:
            if phase != "pull":
                phase = "pull"
                print("phase changed to pull at: ", data[i][1], " second")
        elif abs(float(data[i-1][RWrist_x_index]) - float(data[i][RWrist_x_index])) > 0.015:
            if phase != "relax":
                phase = "relax"
                print("phase changed to relax at: ", data[i][1], " second")
        else:
            pass
        data[i].append(phase)

    headers.append("")
    headers.append("")
    headers.append("Phase")

    #Write the new output file with phase
    output_file = "phased_data.csv"
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(metadata)
        writer.writerow(headers)
        writer.writerow(sub_headers)
        writer.writerows(data)

stroke_count(r"D:\McMaster University\Year 5\5P06A\Virtual_Dragon_Boat_Coach\phased_data.csv")