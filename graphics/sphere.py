"""
graphics/sphere.py
Procedural UV-sphere (latitude / longitude) and the GPU mesh that draws it.

Math (unit sphere, radius = 1)
------------------------------
phi   = latitude,  from +90 deg (north pole) down to -90 deg (south pole)
theta = longitude, from 0 to 360 deg

    x = cos(phi) * cos(theta)
    y = sin(phi)
    z = cos(phi) * sin(theta)

For a sphere centred at the origin the outward normal at a point is the
point itself, so  normal = (x, y, z).

Texture coordinates:  u = theta / 360 deg   (0..1 around the sphere)
                      v = (phi + 90 deg) / 180 deg  (1 at north, 0 at south)

The first and last longitude columns have the same position but different
u (0 and 1), so the seam vertices are duplicated on purpose.
"""

import ctypes
import math

import numpy as np
from OpenGL import GL


def generate_sphere(stacks=32, sectors=64):
    """
    Returns (vertices, indices)
      vertices: float32 array, 8 floats per vertex -> x y z  nx ny nz  u v
      indices : uint32 array, 3 per triangle (counter-clockwise from outside)
    """
    vertices = []
    for i in range(stacks + 1):                      # latitude rings
        phi = math.pi / 2.0 - math.pi * i / stacks   # +90 deg -> -90 deg
        for j in range(sectors + 1):                 # longitude columns
            theta = 2.0 * math.pi * j / sectors

            x = math.cos(phi) * math.cos(theta)
            y = math.sin(phi)
            z = math.cos(phi) * math.sin(theta)

            u = j / sectors
            v = 1.0 - i / stacks
            vertices.extend((x, y, z, x, y, z, u, v))

    indices = []
    for i in range(stacks):
        for j in range(sectors):
            k1 = i * (sectors + 1) + j       # current ring, current column
            k2 = k1 + sectors + 1            # next ring (below), same column
            # Each quad (k1, k1+1, k2, k2+1) is split into two triangles.
            indices.extend((k1, k1 + 1, k2))
            indices.extend((k1 + 1, k2 + 1, k2))

    return (np.array(vertices, dtype=np.float32),
            np.array(indices, dtype=np.uint32))


class SphereMesh:
    """Uploads one unit sphere to the GPU. All bodies share this mesh."""

    def __init__(self, stacks=64, sectors=128):
        vertices, indices = generate_sphere(stacks, sectors)
        self.index_count = int(indices.size)

        self.vao = GL.glGenVertexArrays(1)
        self.vbo = GL.glGenBuffers(1)
        self.ebo = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.vao)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices,
                        GL.GL_STATIC_DRAW)

        # The element buffer binding is stored inside the VAO.
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices,
                        GL.GL_STATIC_DRAW)

        f = vertices.itemsize            # 4 bytes
        stride = 8 * f
        # location 0: position (3 floats)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride,
                                 ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)
        # location 1: normal (3 floats)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride,
                                 ctypes.c_void_p(3 * f))
        GL.glEnableVertexAttribArray(1)
        # location 2: texture coordinate (2 floats)
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