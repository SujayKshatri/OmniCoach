import numpy as np

def calculate_joint_angle(a: list, b: list, c: list) -> float:
    """
    Calculates the 3D angle at joint 'b' given joint coordinates a, b, and c.
    Coordinates must be in [x, y, z] format.
    """
    a = np.array(a)  # e.g., Shoulder
    b = np.array(b)  # e.g., Elbow (Vertex)
    c = np.array(c)  # e.g., Wrist

    # Create vectors
    ba = a - b
    bc = c - b

    # Normalize vectors
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    # Clip to avoid floating point errors outside [-1, 1]
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    
    return float(np.degrees(angle))
