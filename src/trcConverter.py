import csv
import os
import sys

if len(sys.argv) != 3:
    print("Usage: python trcConverter.py <session_id> <trial_name>")
    sys.exit(1)

session_id = sys.argv[1].strip()
trial_name = sys.argv[2].strip()

# Define base data folder where files are downloaded
data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session_id}')

def trc_to_csv(trc_file_path, csv_file_path):
    """
    Convert a .trc file to a .csv file.
    
    :param trc_file_path: Path to the input .trc file
    :param csv_file_path: Path to the output .csv file
    """
    with open(trc_file_path, 'r', encoding='utf-8') as trc_file, open(csv_file_path, 'w', newline='') as csv_file:
        # trc_lines = trc_file.readlines()
        csv_writer = csv.writer(csv_file, delimiter=',')
        
        # Extract the headers and data
        is_data_section = False
        for line in trc_file:
            line = line.strip()
            if not line:
                continue
            if not is_data_section:
                if line.lower().startswith('1'):
                    is_data_section = True
                    csv_writer.writerow(line.split("\t"))
            else:
                # Write numerical data rows into CSV
                csv_writer.writerow(line.split("\t"))
    
    print(f"Converted {trc_file_path} to {csv_file_path} successfully.")

# File paths
trc_file_path = os.path.join(data_folder, 'MarkerData', f'{trial_name}.trc')
csv_file_path = trc_file_path.replace('.trc', '.csv')

# Convert .trc to .csv
trc_to_csv(trc_file_path, csv_file_path)