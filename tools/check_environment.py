"""
tools/check_environment.py
Phase 1 - Environment verification.

Checks, in order:
  1. Python version and architecture
  2. Required libraries and their versions
  3. That GLFW can create an OpenGL 3.3 Core Profile context
  4. That the GPU driver can compile and link a GLSL 330 shader

Run from the project root:   python tools/check_environment.py
Exit code 0 = everything OK, 1 = at least one check failed.
"""

import platform
import sys
from importlib import metadata

OK = "[ OK ]"
WARN = "[WARN]"
FAIL = "[FAIL]"

failures = 0


def report(tag, message):
    """Print one result line and count failures."""
    global failures
    if tag == FAIL:
        failures += 1
    print(f"{tag} {message}")


def section(title):
    print(f"\n=== {title} ===")


# ----------------------------------------------------------------------
# 1. Python
# ----------------------------------------------------------------------
def check_python():
    section("Python")
    v = sys.version_info
    bits = platform.architecture()[0]
    print(f"Python {v.major}.{v.minor}.{v.micro} ({bits}) on "
          f"{platform.system()} {platform.release()}")
    print(f"Interpreter: {sys.executable}")

    if (v.major, v.minor) < (3, 10):
        report(FAIL, "Python 3.10+ is required (3.11 recommended).")
    elif (v.major, v.minor) == (3, 11):
        report(OK, "Python 3.11 (recommended version).")
    else:
        report(WARN, "Python works, but 3.11 is the recommended version.")

    if bits != "64bit":
        report(FAIL, "A 64-bit Python is required.")

    if sys.prefix == sys.base_prefix:
        report(WARN, "You are NOT inside a virtual environment (.venv).")
    else:
        report(OK, "Running inside a virtual environment.")


# ----------------------------------------------------------------------
# 2. Libraries
# ----------------------------------------------------------------------
def check_libraries():
    section("Libraries")
    # (pip distribution name, import name)
    libs = [
        ("PyOpenGL", "OpenGL"),
        ("glfw", "glfw"),
        ("numpy", "numpy"),
        ("pillow", "PIL"),
    ]
    for dist_name, import_name in libs:
        try:
            version = metadata.version(dist_name)
        except metadata.PackageNotFoundError:
            report(FAIL, f"{dist_name} is not installed "
                         f"(run: pip install -r requirements.txt)")
            continue
        try:
            __import__(import_name)
        except Exception as exc:  # import can fail even if installed
            report(FAIL, f"{dist_name} {version} is installed but cannot be "
                         f"imported: {exc}")
            continue
        report(OK, f"{dist_name} {version}")


# ----------------------------------------------------------------------
# 3 + 4. OpenGL context and shader compilation
# ----------------------------------------------------------------------
VERTEX_SRC = """#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

FRAGMENT_SRC = """#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.8, 0.2, 1.0);
}
"""


def compile_shader(GL, source, shader_type):
    """Compile one shader; raise RuntimeError with the driver log on failure."""
    shader = GL.glCreateShader(shader_type)
    GL.glShaderSource(shader, source)
    GL.glCompileShader(shader)
    if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
        log = GL.glGetShaderInfoLog(shader)
        log = log.decode(errors="replace") if isinstance(log, bytes) else log
        GL.glDeleteShader(shader)
        raise RuntimeError(f"Shader compile error:\n{log}")
    return shader


def check_opengl():
    section("OpenGL context (GLFW)")
    try:
        import glfw
        from OpenGL import GL
    except Exception as exc:
        report(FAIL, f"Cannot import glfw / OpenGL: {exc}")
        return

    if not glfw.init():
        report(FAIL, "glfw.init() failed.")
        return

    window = None
    program = None
    try:
        # Ask for OpenGL 3.3 Core Profile; hide the window (test only).
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        window = glfw.create_window(640, 480, "env-check", None, None)
        if not window:
            report(FAIL, "Could not create an OpenGL 3.3 Core context. "
                         "Update your graphics driver (NVIDIA/AMD/Intel) "
                         "and make sure you are not on a Remote Desktop/VM.")
            return
        glfw.make_context_current(window)
        report(OK, "OpenGL 3.3 Core context created.")

        def gl_string(name):
            value = GL.glGetString(name)
            return value.decode(errors="replace") if value else "unknown"

        vendor = gl_string(GL.GL_VENDOR)
        renderer = gl_string(GL.GL_RENDERER)
        version = gl_string(GL.GL_VERSION)
        glsl = gl_string(GL.GL_SHADING_LANGUAGE_VERSION)

        print(f"  Vendor   : {vendor}")
        print(f"  Renderer : {renderer}")
        print(f"  Version  : {version}")
        print(f"  GLSL     : {glsl}")
        print(f"  Max texture size: {GL.glGetIntegerv(GL.GL_MAX_TEXTURE_SIZE)}")

        if "gdi generic" in renderer.lower():
            report(WARN, "Software renderer detected (GDI Generic). "
                         "Performance will be poor - update the GPU driver.")

        # Compile and link a minimal GLSL 330 program.
        try:
            vs = compile_shader(GL, VERTEX_SRC, GL.GL_VERTEX_SHADER)
            fs = compile_shader(GL, FRAGMENT_SRC, GL.GL_FRAGMENT_SHADER)
            program = GL.glCreateProgram()
            GL.glAttachShader(program, vs)
            GL.glAttachShader(program, fs)
            GL.glLinkProgram(program)
            linked = GL.glGetProgramiv(program, GL.GL_LINK_STATUS)
            GL.glDeleteShader(vs)
            GL.glDeleteShader(fs)
            if not linked:
                log = GL.glGetProgramInfoLog(program)
                log = log.decode(errors="replace") if isinstance(log, bytes) else log
                report(FAIL, f"Shader link error:\n{log}")
            else:
                report(OK, "GLSL 330 vertex + fragment shaders compiled and linked.")
        except RuntimeError as exc:
            report(FAIL, str(exc))
    except Exception as exc:
        report(FAIL, f"Unexpected OpenGL error: {exc}")
    finally:
        if program:
            GL.glDeleteProgram(program)
        if window:
            glfw.destroy_window(window)
        glfw.terminate()


def main():
    print("Solar System project - environment check")
    check_python()
    check_libraries()
    check_opengl()

    section("Summary")
    if failures == 0:
        print("All checks passed (warnings, if any, are listed above).")
        return 0
    print(f"{failures} check(s) failed. Fix them before starting Phase 2.")
    return 1


if __name__ == "__main__":
    sys.exit(main())