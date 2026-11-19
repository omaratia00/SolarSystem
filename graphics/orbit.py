"""
graphics/orbit.py
One unit circle (radius 1) in the XZ plane, drawn as a line loop.
Every planet's orbit reuses it: the model matrix scales it to the orbit
radius with Scale(r, 1, r).

Points: (cos(theta), 0, sin(theta)) -- the same parametric equation that
places the planets.
"""

import math

import numpy as np
from OpenGL import GL


class OrbitMesh:
    def __init__(self, segments=360):
        self.segment_count = segments
        points = []
        for i in range(segments):
            theta = 2.0 * math.pi * i / segments
            points.extend((math.cos(theta), 0.0, math.sin(theta)))
        data = np.array(points, dtype=np.float32)

        self.vao = GL.glGenVertexArrays(1)
        self.vbo = GL.glGenBuffers(1)
        GL.glBindVertexArray(self.vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, data.nbytes, data, GL.GL_STATIC_DRAW)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glEnableVertexAttribArray(0)
        GL.glBindVertexArray(0)

    def draw(self):
        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(GL.GL_LINE_LOOP, 0, self.segment_count)
        GL.glBindVertexArray(0)

    def delete(self):
        GL.glDeleteVertexArrays(1, [self.vao])
        GL.glDeleteBuffers(1, [self.vbo])