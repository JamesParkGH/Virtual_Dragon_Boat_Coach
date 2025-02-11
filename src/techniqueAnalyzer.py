import sys
import os
import pandas as pd
from identifyPaddlingSide import identifyPaddlingSide

def techniqueAnalyzer(trc_file, mot_file):
    right_side = identifyPaddlingSide(trc_file)

    # reassign left/right to top/bottom accordingly based on right_side
    return