"""
celestial/saturn_rings.py
Saturn's rings: several flat bands (separate geometry, separate colors),
attached to the planet.
"""

import numpy as np

import config
from core.math3d import scale_uniform
from graphics.ring import RingMesh


class RingBand:
    def __init__(self, inner, outer, color, alpha, segments):
        self.inner = inner
        self.outer = outer
        self.color = np.array(color, dtype=np.float32)
        self.alpha = float(alpha)
        self.mesh = RingMesh(inner, outer, segments)


class SaturnRings:
    def __init__(self, planet):
        self.planet = planet
        self.bands = [RingBand(inner, outer, color, alpha, config.RING_SEGMENTS)
                      for inner, outer, color, alpha in config.SATURN_RING_BANDS]
        self.outer_radius = max(b.outer for b in self.bands)   # in planet radii

    def model_matrix(self):
        """
        The rings move together with Saturn because they use Saturn's
        base matrix (position + axial tilt). The ring geometry is in units
        of Saturn's radius, hence the scale. They do not use the spin
        (added in Phase 5), so only the position/tilt are shared.
        """
        return self.planet.base_matrix() @ scale_uniform(self.planet.radius)

    def delete(self):
        for band in self.bands:
            band.mesh.delete()