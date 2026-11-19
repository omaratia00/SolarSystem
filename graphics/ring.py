"""
graphics/ring.py
A flat ring (annulus) in the XZ plane, used for Saturn's ring bands.

Geometry is defined in units of the planet's radius, so the planet's model
matrix scales it to the right size. Vertex layout matches the sphere
(x y z  nx ny nz  u v) so the same vertex shader can draw it.
"""

import ctypes
import math

import numpy as np
from OpenGL import GL


def generate_ring(inner, outer, segments=256):
    """
    Returns (vertices, indices) for the annulus between `inner` and `outer`.
    For every angle theta there are 2 vertices: one on the inner edge and
    one on the outer edge, so the ring is a strip of quads -> triangles.

    u = theta / 2pi (around the ring), v = 0 inner edge, 1 outer edge
    (ready for a ring texture later). Normal = +Y for every vertex.
    """
    vertices = []
    for j in range(segments + 1):
        theta = 2.0 * math.pi * j / segments
        c, s = math.cos(theta), math.sin(theta)
        u = j / segments
        vertices.extend((inner * c, 0.0, inner * s, 0.0, 1.0, 0.0, u, 0.0))
        vertices.extend((outer * c, 0.0, outer * s, 0.0, 1.0, 0.0, u, 1.0))

    indices = []
    for j in range(segments):
        a = 2 * j          # inner, angle j
        b = 2 * j + 1      # outer, angle j
        c = 2 * j + 2      # inner, angle j+1
        d = 2 * j + 3      # outer, angle j+1
        # Counter-clockwise when seen from above (+Y).
        indices.extend((a, c, b))
        indices.extend((b, c, d))

    return (np.array(vertices, dtype=np.float32),
            np.array(indices, dtype=np.uint32))


class RingMesh:
    def __init__(self, inner, outer, segments=256):
        vertices, indices = generate_ring(inner, outer, segments)
        self.index_count = int(indices.size)

        self.vao = GL.glGenVertexArrays(1)
        self.vbo = GL.glGenBuffers(1)
        self.ebo = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices,
                        GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices,
                        GL.GL_STATIC_DRAW)

        f = vertices.itemsize
        stride = 8 * f
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride,
                                 ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride,
                                 ctypes.c_void_p(3 * f))
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, stride,
                                 ctypes.c_void_p(6 * f))
        GL.glEnableVertexAttribArray(2)
        GL.glBindVertexArray(0)

    def draw(self):
        GL.glBindVertexArray(self.vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index_count,
                          GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        GL.glBindVertexArray(0)

    def delete(self):
        GL.glDeleteVertexArrays(1, [self.vao])
        GL.glDeleteBuffers(2, [self.vbo, self.ebo])