"""
celestial/celestial_body.py
Base class for every sphere in the scene (Sun and planets).
"""

import math

import numpy as np

from core.math3d import rotate_z, scale_uniform, translate


class CelestialBody:
    def __init__(self, name, radius, color, position=(0.0, 0.0, 0.0),
                 emissive=False, axial_tilt_deg=0.0):
        self.name = name
        self.radius = float(radius)
        self.color = np.array(color, dtype=np.float32)
        self.position = np.array(position, dtype=np.float32)
        self.emissive = emissive            # True -> self-lit (the Sun)
        self.axial_tilt_deg = float(axial_tilt_deg)
        # Multiplier of `radius` that covers the whole object (Saturn's
        # rings make it larger than the sphere itself).
        self.extent_scale = 1.0

    @property
    def visual_extent(self):
        return self.radius * self.extent_scale

    def base_matrix(self):
        """
        Translate * RotateZ(tilt)
        Position in the world + tilt of the body's axis. Anything attached
        to the body (like Saturn's rings) starts from this matrix.
        """
        return translate(*self.position) @ rotate_z(math.radians(self.axial_tilt_deg))

    def model_matrix(self):
        """
        Model = Translate * RotateZ(tilt) * Scale
        Applied right-to-left: scale the unit sphere to this body's radius,
        tilt it, then move it to its position in the world.
        (Phase 5 will insert the spin rotation between tilt and scale.)
        """
        return self.base_matrix() @ scale_uniform(self.radius)