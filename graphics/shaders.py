"""
graphics/shaders.py
Loads GLSL source files, compiles and links them into a shader program,
and provides helpers for setting uniforms.
"""

from pathlib import Path

import numpy as np
from OpenGL import GL


def _decode(log):
    return log.decode(errors="replace") if isinstance(log, bytes) else log


class ShaderProgram:
    def __init__(self, vertex_path, fragment_path):
        self._uniform_cache = {}
        self._warned = set()

        vs = self._compile(Path(vertex_path), GL.GL_VERTEX_SHADER)
        fs = self._compile(Path(fragment_path), GL.GL_FRAGMENT_SHADER)

        self.program = GL.glCreateProgram()
        GL.glAttachShader(self.program, vs)
        GL.glAttachShader(self.program, fs)
        GL.glLinkProgram(self.program)

        # Shader objects are no longer needed after linking.
        GL.glDeleteShader(vs)
        GL.glDeleteShader(fs)

        if not GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS):
            log = _decode(GL.glGetProgramInfoLog(self.program))
            raise RuntimeError(f"Shader link error:\n{log}")

    @staticmethod
    def _compile(path, shader_type):
        source = path.read_text(encoding="utf-8")
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            log = _decode(GL.glGetShaderInfoLog(shader))
            GL.glDeleteShader(shader)
            raise RuntimeError(f"Compile error in {path.name}:\n{log}")
        return shader

    def use(self):
        GL.glUseProgram(self.program)

    def _location(self, name):
        if name not in self._uniform_cache:
            loc = GL.glGetUniformLocation(self.program, name)
            if loc == -1 and name not in self._warned:
                # -1 means the name is wrong OR the GLSL compiler removed
                # the uniform because it is never used.
                print(f"[shader warning] uniform '{name}' not found/active.")
                self._warned.add(name)
            self._uniform_cache[name] = loc
        return self._uniform_cache[name]

    # NOTE: the program must be active (call use() first) before setting
    # uniforms.
    def set_float(self, name, value):
        GL.glUniform1f(self._location(name), float(value))

    def set_vec3(self, name, v):
        GL.glUniform3f(self._location(name), float(v[0]), float(v[1]), float(v[2]))

    def set_mat3(self, name, m):
        # Our matrices are row-major NumPy arrays; GL_TRUE tells OpenGL to
        # transpose them into its column-major convention.
        data = np.ascontiguousarray(m, dtype=np.float32)
        GL.glUniformMatrix3fv(self._location(name), 1, GL.GL_TRUE, data)

    def set_mat4(self, name, m):
        data = np.ascontiguousarray(m, dtype=np.float32)
        GL.glUniformMatrix4fv(self._location(name), 1, GL.GL_TRUE, data)

    def delete(self):
        GL.glDeleteProgram(self.program)