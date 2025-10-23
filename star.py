"""
star.py - Main animation and rendering module for the Shooting Star project.
Handles 3D star object rotation, perspective projection, and ASCII rendering 
(including Depth and Lighting).
"""

import math
import time
import sys
import random
from objects import Vec3, Triangle, TRI_OBJ, LENGTH

M_PI: float = math.pi

SCREEN_WIDTH: int = 120
SCREEN_HEIGHT: int = 33
BUFFER_SIZE: int = SCREEN_WIDTH * SCREEN_HEIGHT

output: list = []
z_buffer: list = []

# Rotation angles for X, Y, Z axes
A: float = 0.0
B: float = 0.0
C: float = 0.0
CAMERA_ANGLE: float = 0.0

K1: int = int(SCREEN_WIDTH * LENGTH * 2)
K2: int = int(SCREEN_HEIGHT * LENGTH * 2)

ASPECT_RATIO: float = 0.5

LIGHT_DIR: Vec3 = Vec3(0, 1, -1)
LIGHT_DIR.normalize()

BRIGHTNESS_CHARS: str = ".,-~:;=!*#$@"

NUM_STARS: int = 300
STAR_SPEED: int = 20
STAR_DEPTH_RANGE: int = 200
STAR_Z_MIN: int = -STAR_DEPTH_RANGE
stars: list = []

CAMERA_ORBIT_SPEED: float = M_PI / 200
CAMERA_VERTICAL_SPEED: float = M_PI / 400
CAMERA_VERTICAL_AMOUNT: int = 8
CAMERA_HORIZONTAL_AMOUNT: int = 10


def initialize_stars() -> None:
    global stars
    stars = []
    for _ in range(NUM_STARS):
        x: float = random.uniform(-80, 80)
        y: float = random.uniform(-30, 30)
        z: float = random.uniform(STAR_Z_MIN, -5)
        stars.append(Vec3(x, y, z))


def update_stars() -> None:
    for star in stars:
        star.z += STAR_SPEED
        if star.z > 5:
            star.x = random.uniform(-80, 80)
            star.y = random.uniform(-30, 30)
            star.z = STAR_Z_MIN


def project_star(star: Vec3) -> tuple | None:
    if star.z <= -K2:
        return None
    ooz = 1 / (K2 + star.z)
    perspective_scale = K1 * ooz
    screen_x = star.x * perspective_scale + SCREEN_WIDTH / 2
    screen_y = star.y * perspective_scale * ASPECT_RATIO + SCREEN_HEIGHT / 2
    return screen_x, screen_y, ooz


def render_stars() -> None:
    for star in stars:
        curr_projection = project_star(star)
        if curr_projection is None:
            continue
        
        curr_x, curr_y, curr_ooz = curr_projection
        
        prev_z = star.z - STAR_SPEED
        if prev_z <= -K2:
            prev_z = STAR_Z_MIN
        
        prev_ooz = 1 / (K2 + prev_z)
        prev_perspective_scale = K1 * prev_ooz
        prev_x = star.x * prev_perspective_scale + SCREEN_WIDTH / 2
        prev_y = star.y * prev_perspective_scale * ASPECT_RATIO + SCREEN_HEIGHT / 2
        
        draw_streak(prev_x, prev_y, curr_x, curr_y)


def draw_streak(x_start: float, y_start: float, x_end: float, y_end: float) -> None:
    x_start, y_start, x_end, y_end = int(x_start), int(y_start), int(x_end), int(y_end)
    
    delta_x = abs(x_end - x_start)
    delta_y = abs(y_end - y_start)
    step_x = 1 if x_end > x_start else -1
    step_y = 1 if y_end > y_start else -1
    error = delta_x - delta_y
    
    curr_x = x_start
    curr_y = y_start
    
    while True:
        if 0 <= curr_x < SCREEN_WIDTH and 0 <= curr_y < SCREEN_HEIGHT:
            buffer_index = curr_x + SCREEN_WIDTH * curr_y
            if buffer_index < BUFFER_SIZE:
                output[buffer_index] = '*'
        
        if curr_x == x_end and curr_y == y_end:
            break
        
        error_change = 2 * error
        if error_change > -delta_y:
            error -= delta_y
            curr_x += step_x
        if error_change < delta_x:
            error += delta_x
            curr_y += step_y


def initialize_buffer() -> None:
    global output, z_buffer
    output = [' '] * BUFFER_SIZE
    z_buffer = [float('-inf')] * BUFFER_SIZE


def print_output() -> None:
    print("\x1b[H", end="")  
    for row in range(SCREEN_HEIGHT):
        for col in range(SCREEN_WIDTH):
            print(output[col + SCREEN_WIDTH * row], end="")
        print("")


def update_rotation_angles() -> None:
    global A, B, C, CAMERA_ANGLE
    A += M_PI / 30
    B += M_PI / 50
    C += M_PI / 60
    CAMERA_ANGLE += CAMERA_ORBIT_SPEED


def multiply_matrix_vector(point: Vec3, rotation_matrix: list) -> Vec3:
    x = rotation_matrix[0][0] * point.x + rotation_matrix[0][1] * point.y + rotation_matrix[0][2] * point.z
    y = rotation_matrix[1][0] * point.x + rotation_matrix[1][1] * point.y + rotation_matrix[1][2] * point.z
    z = rotation_matrix[2][0] * point.x + rotation_matrix[2][1] * point.y + rotation_matrix[2][2] * point.z
    return Vec3(x, y, z)


def create_rotation_matrix() -> list:
    cosAx = math.cos(A)
    sinAx = math.sin(A)
    
    cosAy = math.cos(B)
    sinAy = math.sin(B)
    
    cosAz = math.cos(C)
    sinAz = math.sin(C)
    
    return [
        [cosAy * cosAz, sinAx * sinAy * cosAz - cosAx * sinAz, cosAx * sinAy * cosAz + sinAx * sinAz],
        [cosAy * sinAz, sinAx * sinAy * sinAz + cosAx * cosAz, cosAx * sinAy * sinAz - sinAx * cosAz],
        [-sinAy, sinAx * cosAy, cosAx * cosAy]
    ]


def apply_camera_transform(point: Vec3) -> Vec3:
    camera_sway_x = math.cos(CAMERA_ANGLE) * CAMERA_HORIZONTAL_AMOUNT
    camera_bob_y = math.sin(CAMERA_ANGLE * CAMERA_VERTICAL_SPEED / CAMERA_ORBIT_SPEED) * CAMERA_VERTICAL_AMOUNT
    
    point.x -= camera_sway_x
    point.y -= camera_bob_y
    
    return point


def apply_transformation(tri: Triangle, rotation_matrix: list) -> None:
    tri.a = multiply_matrix_vector(tri.a, rotation_matrix)
    tri.b = multiply_matrix_vector(tri.b, rotation_matrix)
    tri.c = multiply_matrix_vector(tri.c, rotation_matrix)
    
    tri.a = apply_camera_transform(tri.a)
    tri.b = apply_camera_transform(tri.b)
    tri.c = apply_camera_transform(tri.c)
    
    tri.normal = tri.calculate_normal()


def get_brightness_character(lighting_value: float) -> str:
    L: float = max(0.1, lighting_value + 1.0)
    L = min(L, 2.0)
    index = int((L - 0.1) * (len(BRIGHTNESS_CHARS) - 1) / 1.9)
    index = max(0, min(index, len(BRIGHTNESS_CHARS) - 1))
    return BRIGHTNESS_CHARS[index]

def project_point(point: Vec3) -> tuple:
        ooz: float = 1 / (K2 + point.z)
        perspective_scale: float = K1 * ooz
        screen_x: float = point.x * perspective_scale + SCREEN_WIDTH / 2
        screen_y: float = point.y * perspective_scale * ASPECT_RATIO + SCREEN_HEIGHT / 2
        return screen_x, screen_y, ooz

def update_output_buffer(triangle: Triangle) -> None:
    if not triangle:
        print("Invalid triangle for output update")
        sys.exit(1)
    
    if triangle.normal.z >= 0:
        return
    
    lighting_value: float = triangle.normal.dot(LIGHT_DIR)
    
    vx1, vy1, d1 = project_point(triangle.a)
    vx2, vy2, d2 = project_point(triangle.b)
    vx3, vy3, d3 = project_point(triangle.c)
    
    avg_depth: float = (d1 + d2 + d3) / 3.0
    
    screen_space_triangle: Triangle = Triangle(
        Vec3(vx1, vy1, 0),
        Vec3(vx2, vy2, 0),
        Vec3(vx3, vy3, 0)
    )
    
    min_x, max_x, min_y, max_y = screen_space_triangle.get_bounding()
    
    min_x = max(0, min_x)
    max_x = min(SCREEN_WIDTH - 1, max_x)
    min_y = max(0, min_y)
    max_y = min(SCREEN_HEIGHT - 1, max_y)
    
    brightness_character: str = get_brightness_character(lighting_value)
    
    for pixel_y in range(min_y, max_y + 1):
        for pixel_x in range(min_x, max_x + 1):
            b_u, b_v, b_w = screen_space_triangle.get_barycentric(float(pixel_x), float(pixel_y))
            
            if (b_u is not None and b_v is not None and b_w is not None and
                b_u >= 0 and b_v >= 0 and b_w >= 0):
                buffer_index: int = pixel_x + SCREEN_WIDTH * pixel_y
                if 0 <= buffer_index < BUFFER_SIZE:
                    if avg_depth > z_buffer[buffer_index]:
                        z_buffer[buffer_index] = avg_depth
                        output[buffer_index] = brightness_character


def main() -> None:
    print("\x1b[2J")
    initialize_stars()
    
    while True:
        start_time: float = time.time()
        
        initialize_buffer()
        render_stars()
        update_stars()
        
        rotation_matrix: list = create_rotation_matrix()    
        
        for tri in TRI_OBJ:
            tri_copy: Triangle = Triangle(
                Vec3(tri.a.x, tri.a.y, tri.a.z),
                Vec3(tri.b.x, tri.b.y, tri.b.z),
                Vec3(tri.c.x, tri.c.y, tri.c.z)
            )
            
            apply_transformation(tri_copy, rotation_matrix)
            update_output_buffer(tri_copy)
        
        print_output()
        
        elapsed: float = time.time() - start_time
        fps: float = 1.0 / elapsed if elapsed > 0 else 0
        print(f"FPS: {fps:.1f}")
        time.sleep(max(0, 1/30 - elapsed))
        update_rotation_angles()


if __name__ == "__main__":
    main()