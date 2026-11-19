"""
celestial/solar_system.py
Builds and owns every object of the system: the Sun, the eight planets,
and Saturn's rings.
"""

import math

import config
from celestial.planet import Planet
from celestial.saturn_rings import SaturnRings
from celestial.sun import Sun


def visual_planet_radius(radius_km):
    """Compressed radius:  0.6 * (R / R_earth) ** 0.4   (see config.py)."""
    ratio = radius_km / config.EARTH_EQUATORIAL_RADIUS_KM
    return config.EARTH_VIS_RADIUS * ratio ** config.PLANET_RADIUS_EXPONENT


def visual_orbit_radius(distance_au):
    """Compressed orbit radius:  base + scale * sqrt(AU)   (see config.py)."""
    return config.ORBIT_BASE + config.ORBIT_SCALE * math.sqrt(distance_au)


class SolarSystem:
    def __init__(self):
        self.sun = Sun()
        self.planets = []
        for data in config.PLANET_DATA:
            self.planets.append(Planet(
                name=data["name"],
                radius=visual_planet_radius(data["radius_km"]),
                color=data["color"],
                orbit_radius=visual_orbit_radius(data["distance_au"]),
                orbit_angle=math.radians(data["start_angle_deg"]),
                axial_tilt_deg=data["axial_tilt_deg"],
            ))

        saturn = next(p for p in self.planets if p.name == "Saturn")
        self.rings = SaturnRings(saturn)
        saturn.extent_scale = self.rings.outer_radius

    @property
    def bodies(self):
        """Sun first, then the planets (everything drawn as a sphere)."""
        return [self.sun] + self.planets

    def delete(self):
        self.rings.delete()