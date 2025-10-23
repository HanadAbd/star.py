"""
objects.py - 3D vector and triangle geometry classes.
Provides core data structures and classes for 3D graphics calculations and mesh operations.
"""
import math

class Vec3:
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def dot(self, other_vector: 'Vec3') -> float:
        dot_product: float = (self.x * other_vector.x + 
                             self.y * other_vector.y + 
                             self.z * other_vector.z)
        return dot_product
    
    def cross(self, other_vector: 'Vec3') -> 'Vec3':
        x: float = self.y * other_vector.z - self.z * other_vector.y
        y: float = self.z * other_vector.x - self.x * other_vector.z
        z: float = self.x * other_vector.y - self.y * other_vector.x
        
        return Vec3(x, y, z)
    
    def normalize(self) -> 'Vec3':
        vector_magnitude = math.sqrt(self.x * self.x + 
                                           self.y * self.y + 
                                           self.z * self.z)
        
        if vector_magnitude > 0:
            self.x /= vector_magnitude
            self.y /= vector_magnitude
            self.z /= vector_magnitude
        
        return self


class Triangle:
    
    def __init__(self, vertex_a: Vec3, vertex_b: Vec3, vertex_c: Vec3) -> None:
        self.a: Vec3 = vertex_a
        self.b: Vec3 = vertex_b
        self.c: Vec3 = vertex_c
        self.normal: Vec3 = self.calculate_normal()
    
    def calculate_normal(self) -> Vec3:
        vec_ab = Vec3(
            self.b.x - self.a.x,
            self.b.y - self.a.y,
            self.b.z - self.a.z
        )
        vec_ac = Vec3(
            self.c.x - self.a.x,
            self.c.y - self.a.y,
            self.c.z - self.a.z
        )
        
        norm = vec_ab.cross(vec_ac)
        norm.normalize()
        
        return norm
    
    def get_bounding(self) -> tuple:
        min_x = int(min(self.a.x, self.b.x, self.c.x))
        max_x = int(max(self.a.x, self.b.x, self.c.x))
        
        min_y = int(min(self.a.y, self.b.y, self.c.y))
        max_y = int(max(self.a.y, self.b.y, self.c.y))
        
        return min_x, max_x, min_y, max_y
    
    def get_barycentric(self, point_x: float, point_y: float) -> tuple:
        edge_ac_x = self.c.x - self.a.x
        edge_ac_y = self.c.y - self.a.y
        edge_ab_x = self.b.x - self.a.x
        edge_ab_y = self.b.y - self.a.y
        edge_ap_x = point_x - self.a.x
        edge_ap_y = point_y - self.a.y
        
        dot_ac_ac = edge_ac_x * edge_ac_x + edge_ac_y * edge_ac_y
        dot_ac_ab = edge_ac_x * edge_ab_x + edge_ac_y * edge_ab_y
        dot_ac_ap = edge_ac_x * edge_ap_x + edge_ac_y * edge_ap_y
        dot_ab_ab = edge_ab_x * edge_ab_x + edge_ab_y * edge_ab_y
        dot_ab_ap = edge_ab_x * edge_ap_x + edge_ab_y * edge_ap_y
        
        denom = dot_ac_ac * dot_ab_ab - dot_ac_ab * dot_ac_ab
        
        if abs(denom) < 1e-10:
            return None, None, None
        
        denom = 1.0 / denom
        alpha = (dot_ab_ab * dot_ac_ap - dot_ac_ab * dot_ab_ap) * denom
        beta = (dot_ac_ac * dot_ab_ap - dot_ac_ab * dot_ac_ap) * denom
        gamma = 1.0 - alpha - beta
        
        return alpha, beta, gamma

LENGTH: float = 10.0

INNER_RADIUS: float = LENGTH * 0.4
APEX_HEIGHT: float = LENGTH * 0.3

top_apex = Vec3(0, APEX_HEIGHT, 0)
bottom_apex = Vec3(0, -APEX_HEIGHT, 0)
center = Vec3(0, 0, 0)

outer_points = []
inner_points = []

for i in range(5):
    angle = 2 * math.pi * i / 5 - math.pi / 2
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    outer_points.append(Vec3(LENGTH * cos_a, 0, LENGTH * sin_a))
    
    inner_angle = angle + math.pi / 5
    cos_i = math.cos(inner_angle)
    sin_i = math.sin(inner_angle)
    inner_points.append(Vec3(INNER_RADIUS * cos_i, 0, INNER_RADIUS * sin_i))

TRI_OBJ = []

for i in range(5):
    outer_current = outer_points[i]
    outer_next = outer_points[(i + 1) % 5]
    
    inner_current = inner_points[i]
    inner_next = inner_points[(i + 1) % 5]
    
    # Top pyramid faces
    TRI_OBJ.append(Triangle(outer_current, top_apex, inner_current))
    TRI_OBJ.append(Triangle(inner_current, top_apex, outer_next))
    
    # Bottom pyramid faces
    TRI_OBJ.append(Triangle(outer_current, inner_current, bottom_apex))
    TRI_OBJ.append(Triangle(inner_current, outer_next, bottom_apex))

# LENGTH: float = 10.0
# HALF_SIZE: float = LENGTH / 2.0

# VERTICES = [
#     Vec3(-HALF_SIZE, -HALF_SIZE, -HALF_SIZE),  # 0
#     Vec3(HALF_SIZE, -HALF_SIZE, -HALF_SIZE),   # 1
#     Vec3(HALF_SIZE, HALF_SIZE, -HALF_SIZE),    # 2
#     Vec3(-HALF_SIZE, HALF_SIZE, -HALF_SIZE),   # 3
#     Vec3(-HALF_SIZE, -HALF_SIZE, HALF_SIZE),   # 4
#     Vec3(HALF_SIZE, -HALF_SIZE, HALF_SIZE),    # 5
#     Vec3(HALF_SIZE, HALF_SIZE, HALF_SIZE),     # 6
#     Vec3(-HALF_SIZE, HALF_SIZE, HALF_SIZE),    # 7
# ]

# TRI_OBJ = [
#     Triangle(VERTICES[0], VERTICES[1], VERTICES[2]),
#     Triangle(VERTICES[0], VERTICES[2], VERTICES[3]),
#     Triangle(VERTICES[5], VERTICES[4], VERTICES[7]),
#     Triangle(VERTICES[5], VERTICES[7], VERTICES[6]),
#     Triangle(VERTICES[4], VERTICES[0], VERTICES[3]),
#     Triangle(VERTICES[4], VERTICES[3], VERTICES[7]),
#     Triangle(VERTICES[1], VERTICES[5], VERTICES[6]),
#     Triangle(VERTICES[1], VERTICES[6], VERTICES[2]),
#     Triangle(VERTICES[3], VERTICES[2], VERTICES[6]),
#     Triangle(VERTICES[3], VERTICES[6], VERTICES[7]),
#     Triangle(VERTICES[4], VERTICES[5], VERTICES[1]),
#     Triangle(VERTICES[4], VERTICES[1], VERTICES[0]),
# ]