"""
celestial/sun.py
The Sun: a self-illuminated body at the centre of the system.
"""

import config
from celestial.celestial_body import CelestialBody


class Sun(CelestialBody):
    def __init__(self):
        super().__init__("Sun", config.SUN_RADIUS, config.SUN_COLOR,
                         position=(0.0, 0.0, 0.0), emissive=True)