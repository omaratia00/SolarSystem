"""
graphics/lighting.py
A point light source (the Sun). The shader does the actual lighting math;
this class only stores the light's parameters.
"""

import numpy as np


class PointLight:
    def __init__(self, position=(0.0, 0.0, 0.0), color=(1.0, 1.0, 1.0),
                 ambient=0.08):
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.ambient = float(ambient)   # minimum light on the dark side