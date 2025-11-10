# star.py: A 3D ASCII Art Rendering Engine

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)

A real-time 3D graphics engine written from scratch in Python. It renders a rotating star in ASCII characters directly in your terminal, complete with simulated lighting, 3D transformations, and a "hyperspace" starfield effect.

> This project was inspired by the legendary `donut.c` by Andy Sloane and was developed to explore the fundamentals of 3D graphics programming.

---

### 📹 Demo

**`![star.gif]`**




- **3D Object Rendering:** Renders a 3D star composed of triangular faces in the terminal.
- **Real-time Transformations:** Applies yaw, pitch, and roll rotations to the star in real-time using rotation matrices calculated from scratch.
- **Dynamic Lighting:** Simulates a light source using the dot product between surface normals and a light vector to create depth and shading.
- **Z-Buffering:** Implements a z-buffer for correct depth sorting, ensuring that closer faces and particles correctly occlude those behind them.
- **Particle System:** Features a background "hyperspace" effect with 300 stars moving toward the viewer, rendered using the Bresenham line algorithm to create motion trails.

## Tech Stack

- **Language:** **Python 3**
- **Core Concepts:**
  - 3D Vector Math (Dot Product, Cross Product)
  - Rotation Matrices & Euler Angles
  - Perspective Projection
  - Gouraud Shading (per-triangle lighting)
  - Z-Buffer (Depth Buffer) Algorithm
  - Bresenham's Line Algorithm

## Getting Started

To run this project locally, follow these simple steps.

### Prerequisites

- Python 3.5+

### Installation & Execution

1. Clone the repository:

    ```sh
    git clone https://github.com/HanadAbd/star.py.git
    ```

2. Navigate to the project directory:

    ```sh
    cd star.py
    ```

3. Run the main script:

    ```sh
    python star.py
    ```

    *Press `CTRL+C` to exit the animation.*

## How It Works

The engine runs in a main loop that updates at a target of 30 frames per second. In each frame, the following steps occur:

1. **Update Angles:** The rotation angles (yaw, pitch, roll) for the star and camera are updated to create continuous animation.
2. **Transform Vertices:** For each triangle that makes up the star, its vertices are transformed by applying the rotation matrices.
3. **Calculate Lighting:** The orientation of each triangle face is used to calculate its brightness relative to a fixed light source. This determines the ASCII character used for rendering (`.`, `:`, `!`, `#`, `$`).
4. **Project to 2D:** The 3D coordinates are projected onto a 2D screen space to be displayed in the terminal.
5. **Render Particles:** The background stars in the particle system are updated, projected, and drawn.
6. **Z-Buffering:** A z-buffer ensures that only the closest pixel (triangle face or particle) is drawn at any given screen coordinate.
7. **Display:** The final buffer is printed to the console, and the process repeats.
