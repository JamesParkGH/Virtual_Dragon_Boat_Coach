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
    RAnkle_x_index = headers.index("RAnkle")
    Time_index = headers.index("Time")

    stroke_time_stamp = {}
    stroke_number = 0
    stroke_interval = 0
    stroke_counted = False

    for i in range(len(data)-3):
        pulling = data[i][RWrist_x_index] > data[i+1][RWrist_x_index] and data[i+1][RWrist_x_index] > data[i+2][RWrist_x_index] and data[i+2][RWrist_x_index] > data[i+3][RWrist_x_index]
        starting = float(data[i][RWrist_x_index]) > float(data[i][RAnkle_x_index])

        if pulling and starting and not stroke_counted:
            stroke_counted = True
            stroke_number += 1
            stroke_info = {stroke_number:data[i][Time_index]}
            stroke_time_stamp.update(stroke_info)
            stroke_interval = 40
            print("marking stroke ", stroke_number, " at time: ", data[i][Time_index], " seconds")
        elif stroke_interval > 0:
            stroke_interval -= 1
            if stroke_interval == 0:
                stroke_counted = False
        else:
            pass
    
    print(stroke_time_stamp)
    return stroke_time_stamp

stroke_count(r"C:\5P06A\git\Virtual_Dragon_Boat_Coach\data\OpenCapData_358018a7-1cc4-4b1c-bb03-982c74c17c49\MarkerData\Ed_paddling.csv")