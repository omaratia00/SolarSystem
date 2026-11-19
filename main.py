"""
main.py
Application entry point.
Phase 4: Sun + 8 planets + orbit lines + Saturn's rings (static positions).

TEMPORARY test controls (the real camera comes in Phase 7):
    0         overview of the whole system
    1 .. 8    focus on Mercury .. Neptune
    9         focus on the Sun
    UP / DOWN zoom in / out
    ESC       quit
"""

import math

import numpy as np

import config
from celestial.solar_system import SolarSystem
from core.math3d import look_at, perspective
from core.renderer import Renderer
from core.window import Window
from graphics.lighting import PointLight


def main():
    window = Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE,
                    config.GL_VERSION_MAJOR, config.GL_VERSION_MINOR,
                    config.MSAA_SAMPLES, config.VSYNC)

    renderer = None
    solar_system = None
    try:
        renderer = Renderer(config.BACKGROUND_COLOR)
        solar_system = SolarSystem()

        # The Sun is the light source: a point light at its position.
        light = PointLight(position=solar_system.sun.position,
                           color=(1.0, 0.95, 0.9), ambient=0.08)

        # ---- temporary camera state ----------------------------------
        focus_name = "Overview"
        focus_target = np.zeros(3, dtype=np.float32)
        focus_body = None
        cam_distance = config.OVERVIEW_DISTANCE
        cam_angle = 0.0
        elevation = math.radians(config.CAMERA_ELEVATION_DEG)
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        last_time = window.get_time()
        fps_timer = 0.0
        frame_count = 0

        while not window.should_close():
            # ---- timing (delta time) --------------------------------
            now = window.get_time()
            dt = now - last_time
            last_time = now

            window.poll_events()

            # ---- temporary input: choose what the camera looks at ----
            for digit in window.consume_digit_presses():
                if digit == 0:
                    focus_name, focus_body = "Overview", None
                    cam_distance = config.OVERVIEW_DISTANCE
                elif digit == 9:
                    focus_body = solar_system.sun
                    focus_name = focus_body.name
                    cam_distance = config.FOCUS_DISTANCE_FACTOR * focus_body.visual_extent
                elif digit <= len(solar_system.planets):
                    focus_body = solar_system.planets[digit - 1]
                    focus_name = focus_body.name
                    cam_distance = config.FOCUS_DISTANCE_FACTOR * focus_body.visual_extent

            # ---- zoom (exponential, frame-rate independent) ----------
            cam_distance *= math.exp(-window.zoom_direction() * config.ZOOM_SPEED * dt)
            cam_distance = min(max(cam_distance, config.MIN_CAMERA_DISTANCE),
                               config.MAX_CAMERA_DISTANCE)

            # ---- update: camera moves on a circle around the target --
            cam_angle = (cam_angle + config.CAMERA_ORBIT_SPEED * dt) % (2.0 * math.pi)
            target = focus_body.position if focus_body is not None else focus_target
            horizontal = cam_distance * math.cos(elevation)
            eye = target + np.array([horizontal * math.cos(cam_angle),
                                     cam_distance * math.sin(elevation),
                                     horizontal * math.sin(cam_angle)],
                                    dtype=np.float32)

            view = look_at(eye, target, up)
            projection = perspective(config.FOV_DEG, window.aspect_ratio,
                                     config.NEAR_PLANE, config.FAR_PLANE)

            # ---- render ---------------------------------------------
            renderer.render(solar_system, view, projection, eye, light)
            window.swap_buffers()

            # ---- FPS display ----------------------------------------
            frame_count += 1
            fps_timer += dt
            if fps_timer >= 0.5:
                fps = frame_count / fps_timer
                window.set_title(f"{config.WINDOW_TITLE} | Focus: {focus_name} "
                                 f"| FPS: {fps:.0f} | dt: {dt * 1000:.1f} ms")
                fps_timer = 0.0
                frame_count = 0
    finally:
        if solar_system:
            solar_system.delete()
        if renderer:
            renderer.delete()
        window.destroy()


if __name__ == "__main__":
    main()