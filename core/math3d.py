"""
core/math3d.py
Hand-written 4x4 transformation matrices (NumPy, float32).

Convention used everywhere in this project
------------------------------------------
* Column vectors:      v' = M @ v      with v = (x, y, z, 1)
* Right-handed system: +X right, +Y up, +Z towards the viewer
* Matrices are stored row-major in NumPy (the "normal math" layout).
  They are uploaded to OpenGL with the transpose flag = GL_TRUE.
* Angles are in RADIANS.

Combining transformations:  M = T @ R @ S   means "scale first, then rotate,
then translate" (matrices are applied right-to-left to the vertex).
"""

import math

import numpy as np


def identity():
    return np.identity(4, dtype=np.float32)


def normalize(v):
    v = np.asarray(v, dtype=np.float32)
    length = np.linalg.norm(v)
    if length == 0.0:
        return v
    return v / length


# ----------------------------------------------------------------------
# Basic transformations
# ----------------------------------------------------------------------
def translate(x, y, z):
    """
    | 1 0 0 tx |
    | 0 1 0 ty |
    | 0 0 1 tz |
    | 0 0 0 1  |
    """
    m = identity()
    m[0, 3] = x
    m[1, 3] = y
    m[2, 3] = z
    return m


def scale(sx, sy, sz):
    """
    | sx 0  0  0 |
    | 0  sy 0  0 |
    | 0  0  sz 0 |
    | 0  0  0  1 |
    """
    m = identity()
    m[0, 0] = sx
    m[1, 1] = sy
    m[2, 2] = sz
    return m


def scale_uniform(s):
    return scale(s, s, s)


def rotate_x(angle):
    c, s = math.cos(angle), math.sin(angle)
    m = identity()
    m[1, 1], m[1, 2] = c, -s
    m[2, 1], m[2, 2] = s, c
    return m


def rotate_y(angle):
    c, s = math.cos(angle), math.sin(angle)
    m = identity()
    m[0, 0], m[0, 2] = c, s
    m[2, 0], m[2, 2] = -s, c
    return m


def rotate_z(angle):
    c, s = math.cos(angle), math.sin(angle)
    m = identity()
    m[0, 0], m[0, 1] = c, -s
    m[1, 0], m[1, 1] = s, c
    return m


# ----------------------------------------------------------------------
# Camera matrices
# ----------------------------------------------------------------------
def look_at(eye, target, up):
    """
    View matrix. Builds the camera's orthonormal basis (right, true_up,
    -forward) and moves the whole world so the camera sits at the origin
    looking down -Z.
    """
    eye = np.asarray(eye, dtype=np.float32)
    target = np.asarray(target, dtype=np.float32)

    forward = normalize(target - eye)
    right = normalize(np.cross(forward, up))
    true_up = np.cross(right, forward)

    m = identity()
    m[0, :3] = right
    m[1, :3] = true_up
    m[2, :3] = -forward
    m[0, 3] = -np.dot(right, eye)
    m[1, 3] = -np.dot(true_up, eye)
    m[2, 3] = np.dot(forward, eye)
    return m


def perspective(fov_deg, aspect, near, far):
    """
    Perspective projection matrix (maps the view frustum to clip space).
    f = 1 / tan(fov/2)

    | f/aspect  0   0                  0                 |
    | 0         f   0                  0                 |
    | 0         0   (far+near)/(near-far)  2*far*near/(near-far) |
    | 0         0   -1                 0                 |
    """
    f = 1.0 / math.tan(math.radians(fov_deg) / 2.0)
    m = np.zeros((4, 4), dtype=np.float32)
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2.0 * far * near) / (near - far)
    m[3, 2] = -1.0
    return m


def normal_matrix(model):
    """
    Matrix used to transform normals: inverse-transpose of the upper-left
    3x3 part of the model matrix. It keeps normals perpendicular to the
    surface even when the model uses non-uniform scaling.
    """
    upper = np.asarray(model, dtype=np.float32)[:3, :3]
    return np.linalg.inv(upper).T.astype(np.float32)