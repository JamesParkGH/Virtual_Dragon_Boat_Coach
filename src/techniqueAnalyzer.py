import sys
import os
import pandas as pd
from identifyPaddlingSide import identifyPaddlingSide

def techniqueAnalyzer(trc_file, mot_file):
    right_side = identifyPaddlingSide(trc_file)

    # non-side data
    
    # top-side data

    # bottom-side data

    # reassign left/right to top/bottom accordingly based on right_side
    return