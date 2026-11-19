"""
config.py
Central place for all tunable settings, so no "magic numbers" are
scattered across the project.
"""

import math
from pathlib import Path

# ---- Paths ----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
SHADER_DIR = BASE_DIR / "assets" / "shaders"
TEXTURE_DIR = BASE_DIR / "assets" / "textures"

# ---- Window ---------------------------------------------------------
WINDOW_TITLE = "3D Animated Solar System"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
VSYNC = True            # True: sync with monitor refresh rate
MSAA_SAMPLES = 4        # multisample anti-aliasing (smoother edges)

# ---- OpenGL ---------------------------------------------------------
GL_VERSION_MAJOR = 3
GL_VERSION_MINOR = 3

# ---- Rendering ------------------------------------------------------
BACKGROUND_COLOR = (0.01, 0.01, 0.04, 1.0)   # very dark blue (space)
SPHERE_STACKS = 64      # latitude subdivisions
SPHERE_SECTORS = 128    # longitude subdivisions
ORBIT_SEGMENTS = 360    # points on each orbit circle
RING_SEGMENTS = 256     # subdivisions around each Saturn ring band

# ---- Projection -----------------------------------------------------
FOV_DEG = 45.0
NEAR_PLANE = 0.1
FAR_PLANE = 1000.0

# ---- Phase 4 TEMPORARY camera (replaced by a real camera in Phase 7) -
CAMERA_ELEVATION_DEG = 30.0                  # angle above the orbital plane
CAMERA_ORBIT_SPEED = math.radians(10.0)      # radians per SECOND
OVERVIEW_DISTANCE = 130.0                    # camera distance, whole system
FOCUS_DISTANCE_FACTOR = 5.0                  # distance = factor * body size
MIN_CAMERA_DISTANCE = 1.5
MAX_CAMERA_DISTANCE = 400.0
ZOOM_SPEED = 1.0                             # exponential zoom rate per second

# ======================================================================
# VISUALIZATION SCALE  (NOT real astronomical proportions!)
# ======================================================================
# Real sizes and distances differ by factors of thousands, so everything
# is compressed to keep all planets visible:
#
#   planet radius  = EARTH_VIS_RADIUS * (R_real / R_earth) ** PLANET_RADIUS_EXPONENT
#   orbit radius   = ORBIT_BASE + ORBIT_SCALE * sqrt(distance_in_AU)
#
# Orbits are perfect circles in one plane (real orbits are ellipses with
# small inclinations). The Sun is also drawn far smaller than in reality.
SUN_RADIUS = 4.0
SUN_COLOR = (1.0, 0.75, 0.2)

EARTH_EQUATORIAL_RADIUS_KM = 6378.1
EARTH_VIS_RADIUS = 0.6
PLANET_RADIUS_EXPONENT = 0.4
ORBIT_BASE = 6.0
ORBIT_SCALE = 9.0

# Real data (approximate): equatorial radius [km], mean distance from the
# Sun [AU], axial tilt [degrees]. Colors are visual approximations.
# start_angle_deg is only the initial position on the orbit.
PLANET_DATA = [
    dict(name="Mercury", radius_km=2439.7,  distance_au=0.387,  axial_tilt_deg=0.03,
         color=(0.60, 0.58, 0.55), start_angle_deg=20.0),
    dict(name="Venus",   radius_km=6051.8,  distance_au=0.723,  axial_tilt_deg=177.4,
         color=(0.90, 0.78, 0.50), start_angle_deg=100.0),
    dict(name="Earth",   radius_km=6378.1,  distance_au=1.000,  axial_tilt_deg=23.44,
         color=(0.20, 0.45, 0.85), start_angle_deg=200.0),
    dict(name="Mars",    radius_km=3396.2,  distance_au=1.524,  axial_tilt_deg=25.19,
         color=(0.80, 0.35, 0.20), start_angle_deg=280.0),
    dict(name="Jupiter", radius_km=71492.0, distance_au=5.203,  axial_tilt_deg=3.13,
         color=(0.80, 0.65, 0.50), start_angle_deg=50.0),
    dict(name="Saturn",  radius_km=60268.0, distance_au=9.537,  axial_tilt_deg=26.73,
         color=(0.90, 0.80, 0.55), start_angle_deg=150.0),
    dict(name="Uranus",  radius_km=25559.0, distance_au=19.191, axial_tilt_deg=97.77,
         color=(0.55, 0.82, 0.85), start_angle_deg=240.0),
    dict(name="Neptune", radius_km=24764.0, distance_au=30.069, axial_tilt_deg=28.32,
         color=(0.25, 0.35, 0.85), start_angle_deg=320.0),
]

# ---- Orbit lines ----------------------------------------------------
ORBIT_COLOR = (0.35, 0.45, 0.60)

# ---- Saturn rings ---------------------------------------------------
# (inner, outer, color, alpha). Radii are in units of SATURN's radius
# (approximate real values: C ring, B ring split in two shades, then the
# Cassini Division gap 1.95-2.03 left empty, then the A ring).
SATURN_RING_BANDS = [
    (1.24, 1.53, (0.45, 0.40, 0.35), 0.35),   # C ring (faint)
    (1.53, 1.75, (0.70, 0.62, 0.50), 0.80),   # B ring, inner part
    (1.75, 1.95, (0.85, 0.76, 0.60), 0.90),   # B ring, outer part (brightest)
    (2.03, 2.27, (0.75, 0.68, 0.55), 0.65),   # A ring
]