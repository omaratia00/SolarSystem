"""
celestial/planet.py
A planet that sits on a circular orbit around the Sun.
"""

import math

from celestial.celestial_body import CelestialBody


class Planet(CelestialBody):
    def __init__(self, name, radius, color, orbit_radius, orbit_angle=0.0,
                 axial_tilt_deg=0.0):
        super().__init__(name, radius, color, axial_tilt_deg=axial_tilt_deg)
        self.orbit_radius = float(orbit_radius)
        self.orbit_angle = float(orbit_angle)      # theta, in radians
        self.update_position()

    def update_position(self):
        """
        Parametric equation of a circle in the XZ plane (Sun at the origin):
            x = r * cos(theta)
            z = r * sin(theta)
        Phase 5 will change theta every frame (theta += speed * dt).
        """
        self.position[0] = self.orbit_radius * math.cos(self.orbit_angle)
        self.position[1] = 0.0
        self.position[2] = self.orbit_radius * math.sin(self.orbit_angle)