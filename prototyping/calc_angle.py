import numpy as np

def calculate_angle(start, middle, end):
    v1 = middle - start
    v2 = end - middle
    dot_prod = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)
    cos_angle = dot_prod / (magnitude_v1*magnitude_v2)
    angle_rad = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)

    return angle_deg