# 3D Animated Solar System

University Computer Graphics project: an interactive 3D Solar System built with
Python, OpenGL 3.3 (Core Profile), GLFW and NumPy.

> Status: work in progress (Phase 3 of 10: Sun + one planet, lighting, perspective).
> Sizes and distances are NOT to real astronomical scale.

## Requirements
- Windows, Python 3.11, a GPU/driver supporting OpenGL 3.3+

## Setup
```powershell
git clone https://github.com/<omar_atia>/SolarSystem.git
cd SolarSystem
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python tools/check_environment.py
python main.py
```

## Project structure
See the folders: `core/`, `celestial/`, `graphics/`, `assets/shaders/`, `tools/`.