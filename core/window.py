"""
core/window.py
Wraps GLFW: window creation, OpenGL context, resize handling, and
basic event/timing helpers.
"""

import glfw
from OpenGL import GL


class Window:
    def __init__(self, width, height, title,
                 gl_major=3, gl_minor=3, samples=4, vsync=True):
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW.")

        # Ask for a Core Profile context (modern OpenGL, shaders only).
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, gl_major)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, gl_minor)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.SAMPLES, samples)

        self.title = title
        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            raise RuntimeError("Failed to create the GLFW window "
                               "(run tools/check_environment.py).")

        glfw.make_context_current(self.handle)
        glfw.swap_interval(1 if vsync else 0)

        self._digit_presses = []     # TEMPORARY (Phase 4), see below

        # Register callbacks.
        glfw.set_framebuffer_size_callback(self.handle, self._on_framebuffer_resize)
        glfw.set_key_callback(self.handle, self._on_key)

        # IMPORTANT: use the FRAMEBUFFER size (pixels), not the window size
        # (screen coordinates). They differ on high-DPI displays.
        self.width, self.height = glfw.get_framebuffer_size(self.handle)
        GL.glViewport(0, 0, self.width, self.height)

    # ---- callbacks --------------------------------------------------
    def _on_framebuffer_resize(self, window, width, height):
        # A minimized window reports 0x0; ignore it to avoid divide-by-zero.
        if width == 0 or height == 0:
            return
        self.width, self.height = width, height
        GL.glViewport(0, 0, width, height)

    def _on_key(self, window, key, scancode, action, mods):
        # Temporary: key handling lives here until core/input_handler.py
        # is written in Phase 7.
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
        elif glfw.KEY_0 <= key <= glfw.KEY_9:
            self._digit_presses.append(key - glfw.KEY_0)

    # ---- TEMPORARY test helpers (Phase 4) ----------------------------
    def consume_digit_presses(self):
        """Digits (0-9) pressed since the last call, in order."""
        digits, self._digit_presses = self._digit_presses, []
        return digits

    def zoom_direction(self):
        """+1 while UP is held (zoom in), -1 while DOWN is held, else 0."""
        direction = 0
        if glfw.get_key(self.handle, glfw.KEY_UP) == glfw.PRESS:
            direction += 1
        if glfw.get_key(self.handle, glfw.KEY_DOWN) == glfw.PRESS:
            direction -= 1
        return direction

    # ---- helpers ----------------------------------------------------
    @property
    def aspect_ratio(self):
        return self.width / self.height if self.height else 1.0

    def should_close(self):
        return glfw.window_should_close(self.handle)

    def poll_events(self):
        glfw.poll_events()

    def swap_buffers(self):
        glfw.swap_buffers(self.handle)

    @staticmethod
    def get_time():
        """Seconds since glfw.init() (high-resolution timer)."""
        return glfw.get_time()

    def set_title(self, title):
        glfw.set_window_title(self.handle, title)

    def destroy(self):
        glfw.destroy_window(self.handle)
        glfw.terminate()