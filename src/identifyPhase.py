import sys
import os
import pandas as pd
from identifyPaddlingSide import identifyPaddlingSide
from strokeCounter import strokeCounter

def identifyPhase(trc_file_path):
    """
    Identify the phase (pull or recovery) for each frame in the TRC file.
    
    Args:
        trc_file_path: Path to the TRC file
        
    Returns:
        A list of phases, one for each frame in the TRC file
    """
    try:
        # Read the TRC file
        df = pd.read_csv(trc_file_path, sep=",", engine="python", header=None)
        
        # Identify indices (y and z not used for now)
        if identifyPaddlingSide(trc_file_path):
            bottom_wrist_x_index = df.iloc[:,11]    # right wrist
        else:
            bottom_wrist_x_index = df.iloc[:,20]    # left wrist
        
        stroke_count, stroke_frames = strokeCounter(trc_file_path)

        phase = "None"
        phase_list = []
        
        # Add initial phase for the first frame
        phase_list.append(phase)
        
        # Analyze subsequent frames
        for i in range(1, df.shape[0]):
            # Compare the x value between the data points
            if float(bottom_wrist_x_index[i-1]) - float(bottom_wrist_x_index[i]) > 0.015:
                if phase != "pull":
                    phase = "pull"
            elif float(bottom_wrist_x_index[i]) - float(bottom_wrist_x_index[i-1]) > 0.015:
                if phase != "recovery":
                    phase = "recovery"
            # If no significant change, keep the current phase
            
            phase_list.append(phase)

        # More paddling phases: Exit, Set up, Catch?
        # 
        # for i in range(1, stroke_count):
        #     # Split up range of each stroke
        #     for frame in range(stroke_frames[i-1], stroke_frames[i]):
        #     # Split pulling frames
        #         curr_stroke = 
        #         halfway = (stroke_frames[i] - stroke_frames[i-1])/2 + stroke_frames[i-1]
        #         if frame <= halfway:
        #             phase_list
        
        return phase_list
    
    except Exception as e:
        print(f"Error in identifyPhase for file {trc_file_path}: {e}")
        # Return a default phase list if an error occurs
        return ["None"] * (len(df) if 'df' in locals() else 100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python identifyPhase.py <trc_file_path>")
        sys.exit(1)

    trc_file_path = sys.argv[1].strip()

    # Ensure the CSV file exists
    if not os.path.exists(trc_file_path):
        print(f"Error: CSV file not found: {trc_file_path}")
        sys.exit(1)
        
    phases = identifyPhase(trc_file_path)
