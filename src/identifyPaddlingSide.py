import sys
import os
import pandas as pd

def identifyPaddlingSide(trc_file_path):
    try:
        # Read through .trc to find which side is the top vs bottom (get avg y_value)
        df = pd.read_csv(trc_file_path, sep=",", engine="python", header=None, index_col=0)

        right_wrist = df.iloc[:, 11]
        left_wrist = df.iloc[:, 20]

        avg_right = right_wrist.sum() / len(right_wrist)
        avg_left = left_wrist.sum() / len(left_wrist)

        right_side = avg_right < avg_left  # Check calibration

        return right_side
    except Exception as e:
        print(f"Error reading or processing file {trc_file_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python identifyPaddlingSide.py <trc_file_path>")
        sys.exit(1)

    trc_file_path = sys.argv[1].strip()

    # Ensure the CSV file exists
    if not os.path.exists(trc_file_path):
        print(f"Error: CSV file not found: {trc_file_path}")
        sys.exit(1)

    # Identify paddling side
    right_side = identifyPaddlingSide(trc_file_path)
    print(f"Paddling on the right side: {right_side}")
