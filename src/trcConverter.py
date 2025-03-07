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
    with open(trc_file_path, 'r') as trc_file, open(csv_file_path, 'w', newline='') as csv_file:
        trc_lines = trc_file.readlines()
        csv_writer = csv.writer(csv_file)
        
        # Extract the headers and data
        is_data_section = False
        for line in trc_lines:
            if not is_data_section:
                # Write header rows (metadata and column headers) into CSV
                csv_writer.writerow(line.strip().split("\t"))
                if line.lower().startswith('frame#'):  # Identify the start of the data section
                    is_data_section = True
            else:
                # Write numerical data rows into CSV
                csv_writer.writerow(line.strip().split("\t"))
    
    print(f"Converted {trc_file_path} to {csv_file_path} successfully.")

# File paths
trc_file_path = os.path.join(data_folder, 'MarkerData', f'{trial_name}.trc')
csv_file_path = trc_file_path.replace('.trc', '.csv')

# Convert .trc to .csv
trc_to_csv(trc_file_path, csv_file_path)