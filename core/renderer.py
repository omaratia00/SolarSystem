"""
core/renderer.py
Owns global OpenGL state, the shared meshes, the shader programs, and
draws the whole solar system.

Draw order matters:
  1. opaque spheres (Sun, planets)      -> write to the depth buffer
  2. orbit lines                        -> depth-tested against the spheres
  3. transparent Saturn rings (last)    -> blended, no depth writes
"""

from OpenGL import GL

import config
from core.math3d import normal_matrix, scale
from graphics.orbit import OrbitMesh
from graphics.shaders import ShaderProgram
from graphics.sphere import SphereMesh


class Renderer:
    def __init__(self, clear_color):
        GL.glEnable(GL.GL_DEPTH_TEST)    # hidden-surface removal (Z-buffer)
        GL.glDepthFunc(GL.GL_LESS)       # keep the fragment that is closer
        GL.glEnable(GL.GL_CULL_FACE)     # skip triangles facing away
        GL.glCullFace(GL.GL_BACK)
        GL.glFrontFace(GL.GL_CCW)        # counter-clockwise = front face
        GL.glEnable(GL.GL_MULTISAMPLE)   # anti-aliasing (needs MSAA hint)
        GL.glClearColor(*clear_color)
        self._print_info()

        self.sphere = SphereMesh(config.SPHERE_STACKS, config.SPHERE_SECTORS)
        self.orbit_mesh = OrbitMesh(config.ORBIT_SEGMENTS)

        sd = config.SHADER_DIR
        self.lit_shader = ShaderProgram(sd / "body.vert", sd / "lit.frag")
        self.sun_shader = ShaderProgram(sd / "body.vert", sd / "sun.frag")
        self.ring_shader = ShaderProgram(sd / "body.vert", sd / "ring.frag")
        self.orbit_shader = ShaderProgram(sd / "orbit.vert", sd / "orbit.frag")

    @staticmethod
    def _print_info():
        def s(name):
            value = GL.glGetString(name)
            return value.decode(errors="replace") if value else "unknown"

        print("OpenGL renderer :", s(GL.GL_RENDERER))
        print("OpenGL version  :", s(GL.GL_VERSION))
        print("GLSL version    :", s(GL.GL_SHADING_LANGUAGE_VERSION))

    def render(self, solar_system, view, projection, camera_pos, light):
        """Draw one complete frame."""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        # ---- per-frame uniforms ---------------------------------------
        for shader in (self.lit_shader, self.sun_shader,
                       self.ring_shader, self.orbit_shader):
            shader.use()
            shader.set_mat4("uView", view)
            shader.set_mat4("uProjection", projection)

        for shader in (self.lit_shader, self.sun_shader):
            shader.use()
            shader.set_vec3("uViewPos", camera_pos)

        for shader in (self.lit_shader, self.ring_shader):
            shader.use()
            shader.set_vec3("uLightPos", light.position)
            shader.set_vec3("uLightColor", light.color)
            shader.set_float("uAmbient", light.ambient)

        # ---- 1. opaque spheres ------------------------------------------
        for body in solar_system.bodies:
            shader = self.sun_shader if body.emissive else self.lit_shader
            shader.use()
            model = body.model_matrix()
            shader.set_mat4("uModel", model)
            shader.set_mat3("uNormalMatrix", normal_matrix(model))
            shader.set_vec3("uColor", body.color)
            self.sphere.draw()

        # ---- 2. orbit lines ---------------------------------------------
        self.orbit_shader.use()
        self.orbit_shader.set_vec3("uColor", config.ORBIT_COLOR)
        for planet in solar_system.planets:
            r = planet.orbit_radius
            self.orbit_shader.set_mat4("uModel", scale(r, 1.0, r))
            self.orbit_mesh.draw()

        # ---- 3. transparent rings ---------------------------------------
        rings = solar_system.rings
        GL.glDisable(GL.GL_CULL_FACE)             # visible from both sides
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glDepthMask(GL.GL_FALSE)               # test depth, don't write it

        self.ring_shader.use()
        model = rings.model_matrix()
        self.ring_shader.set_mat4("uModel", model)
        self.ring_shader.set_mat3("uNormalMatrix", normal_matrix(model))
        for band in rings.bands:
            self.ring_shader.set_vec3("uColor", band.color)
            self.ring_shader.set_float("uAlpha", band.alpha)
            band.mesh.draw()

        GL.glDepthMask(GL.GL_TRUE)
        GL.glDisable(GL.GL_BLEND)
        GL.glEnable(GL.GL_CULL_FACE)

    def delete(self):
        self.sphere.delete()
        self.orbit_mesh.delete()
        for shader in (self.lit_shader, self.sun_shader,
                       self.ring_shader, self.orbit_shader):
            shader.delete()