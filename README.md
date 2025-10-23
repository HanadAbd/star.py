# Shooting Star: A 3D ASCII Art Visualization

#### Video Demo:  {https://www.youtube.com/watch?v=ug0PBCDaRJc}

#### Description:

My project is a python-based 3D graphics project that brings the classic ASCII art animation, inspired by the legendary `donut.c` program that renders a spinning donut in ASCII characters, this project transforms that concept into a rotating 5-pointed star surrounded by a field of streaking stars that fly toward the viewer. Main difference being being that `donut.c` uses point rasterization, with mine using triangular rasterization, since that allows me to draw faces, instead of just points. Again the star 

The project showcases how complex 3D visualization can be achieved using only a command-line interface and only requires python (maybe specifically python 3.5+ to account for types), combining mathematical precision with flashy visual effects. The spinning star is constructed from triangular faces arranged in a star polyhedron configuration, with  lighting from above and behind that creates depth and dimension. Simultaneously, a particle system simulates hundreds of stars moving through space, creating a hyperspace-like effect that makes the viewer feel as though they are traveling through the star field. It's meant to look like a shooting star, or a star travelling amongst other stars.

**Core Features:**

The main visualization features a dynamically rotating 5-pointed star that orbits through space with a bobbing camera effect. The star is geometrically defined as a compound of two pyramids (top and bottom apexes) connected by an outer and inner ring of vertices, creating the classic 5-pointed star shape. The camera system rotates around the star while also moving up and down, creating a more engaging viewing experience than a static perspective.

The literal approach is, having a long list of "triangles", which are simply comprised of 3 vertices. You can represent any 3d object with this approach, so in this case, a star. And we can use rotation matrix multiplication to rotate each point for every triangle, each frame. Hence making the entire object. This is the easier part and mostly a copy of `donut.c`. You then must map those coordinates to the (x,y) coordinates of the screen (which is represented as a array treated as a double array). This is done with a bounding box (getting min/max xy of triangle) and using barycentric coordinates, to determine if a pixel is, or isn't in the triangle. This also allows us to calculate depth, to see which triangle is on top of each other.

Additionally, 300 stars are continuously rendered, moving toward the viewer and creating motion trails through the Bresenham line algorithm, simulating a hyperspace jump effect. Although it's a small touch, there is also an oscillating "movement" to make the object more dynamic, although it's not the object moving the camera itself rotating.

**Design Choices and Technical Implementation:**

For the 3D transformations, I implemented a complete rotation matrix system that applies yaw, pitch, and roll rotations to all vertices for each triangle for each frame. Rather than using external graphics libraries, all mathematics is implemented from scratch using vector operations (dot products, cross products, normalization) and matrix multiplication.

The lighting system uses dot product calculations between surface normal and a light direction vector to determine brightness levels. This per-triangle lighting creates the illusion of depth and three-dimensionality on the flat terminal display. The brightness is mapped to a character set (`.,-~:;=!*#$@`) where darker characters represent less-lit faces and brighter characters represent well-lit faces.

The star field effect was implemented using a particle system where each "star" is tracked with its 3D position, projected onto the 2D screen, and rendered as a motion trail using the Bresenham line-drawing algorithm. The algorithm walks between the star's previous and current positions, plotting points along the line to create the streak effect. Stars wrap around when they pass the viewer, recycling back to the far distance with random positions to maintain the continuous effect.

The z-buffer implementation ensures proper depth sorting. Triangles are only rendered if they are closer to the viewer than previously rendered geometry at that screen position. Thus preventing the back-facing sides of the star from incorrectly appearing in front of the front-facing triangles.

**File Descriptions:**

`star.py` is the main rendering engine and entry point for the program. This file contains all the animation logic, including the main loop that runs at 30 FPS, the rotation variables updates that control the star's spin, the star field initialization and update system, and the core rendering functions. It orchestrates the rotation matrices, applies camera transformations, projects 3D geometry onto the 2D screen, manages the output buffer and z-buffer, and handles terminal output using ANSI escape codes to clear and reposition the cursor.

`objects.py` defines the fundamental mathematical and geometric components used throughout the project. The `Vec3` class represents three-dimensional vectors with dot product, cross product, and normalization methods. The `Triangle` class represents triangular faces with methods to calculate surface normal (critical for lighting), compute bounding boxes (optimization for rasterization), and calculate barycentric coordinates. The bottom half of `objects.py` constructs the 5-pointed star geometry by calculating the positions of outer and inner ring vertices around a circle, then creating triangular faces for both the top and bottom pyramids.
