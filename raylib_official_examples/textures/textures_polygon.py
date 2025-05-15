"""raylib [textures] example - Draw Textured Polygon
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 3.7, last time updated with raylib 3.7
Example contributed by Chris Camacho (@chriscamacho) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Chris Camacho (@chriscamacho) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

MAX_POINTS = 11      # 10 points and back to the start

# Draw textured polygon, defined by vertex and texture coordinates
def draw_texture_poly(texture, center, points, texcoords, point_count, tint):
    # Notice the "rl." prefix for the rlgl functions
    rl.rl_begin(rl.RL_TRIANGLES)
    
    rl.rl_set_texture(texture.id)
    
    rl.rl_color4ub(tint[0], tint[1], tint[2], tint[3])
    
    for i in range(point_count - 1):
        rl.rl_tex_coord2f(0.5, 0.5)
        rl.rl_vertex2f(center.x, center.y)
        
        rl.rl_tex_coord2f(texcoords[i].x, texcoords[i].y)
        rl.rl_vertex2f(points[i].x + center.x, points[i].y + center.y)
        
        rl.rl_tex_coord2f(texcoords[i + 1].x, texcoords[i + 1].y)
        rl.rl_vertex2f(points[i + 1].x + center.x, points[i + 1].y + center.y)
    
    rl.rl_end()
    
    rl.rl_set_texture(0)

# Initialization
screenWidth = 800
screenHeight = 450

rl.init_window(screenWidth, screenHeight, "raylib [textures] example - textured polygon")

# Define texture coordinates to map our texture to poly
texcoords = [
    rl.Vector2(0.75, 0.0),
    rl.Vector2(0.25, 0.0),
    rl.Vector2(0.0, 0.5),
    rl.Vector2(0.0, 0.75),
    rl.Vector2(0.25, 1.0),
    rl.Vector2(0.375, 0.875),
    rl.Vector2(0.625, 0.875),
    rl.Vector2(0.75, 1.0),
    rl.Vector2(1.0, 0.75),
    rl.Vector2(1.0, 0.5),
    rl.Vector2(0.75, 0.0)  # Close the poly
]

# Define the base poly vertices from the UV's
# NOTE: They can be specified in any other way
points = []
for i in range(MAX_POINTS):
    points.append(rl.Vector2(
        (texcoords[i].x - 0.5) * 256.0,
        (texcoords[i].y - 0.5) * 256.0
    ))

# Define the vertices drawing position
# NOTE: Initially same as points but updated every frame
positions = []
for i in range(MAX_POINTS):
    positions.append(rl.Vector2(points[i].x, points[i].y))

# Load texture to be mapped to poly
texture = rl.load_texture(str(THIS_DIR/"resources/cat.png"))

angle = 0.0  # Rotation angle (in degrees)

rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not rl.window_should_close():  # Detect window close button or ESC key
    # Update
    # Update points rotation with an angle transform
    # NOTE: Base points position are not modified
    angle += 1.0
    for i in range(MAX_POINTS):
        # Convert angle from degrees to radians for rotation
        positions[i] = rl.vector2_rotate(points[i], angle * math.pi/180)
    
    # Draw
    rl.begin_drawing()
    
    rl.clear_background(rl.RAYWHITE)
    
    rl.draw_text("textured polygon", 20, 20, 20, rl.DARKGRAY)
    
    draw_texture_poly(
        texture, 
        rl.Vector2(rl.get_screen_width()/2.0, rl.get_screen_height()/2.0),
        positions, texcoords, MAX_POINTS, rl.WHITE
    )
    
    rl.end_drawing()

# De-Initialization
rl.unload_texture(texture)  # Unload texture
rl.close_window()  # Close window and OpenGL context