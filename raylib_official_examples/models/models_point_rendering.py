"""raylib example - point rendering
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.0, last time updated with raylib 5.0
Example contributed by Reese Gallagher (@satchelfrost) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 Reese Gallagher (@satchelfrost)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
import random
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

MAX_POINTS = 10000000    # 10 million
MIN_POINTS = 1000        # 1 thousand

# Generate mesh using points
def gen_mesh_points(num_points):
    mesh = rl.Mesh()
    mesh.triangleCount = 1
    mesh.vertexCount = num_points
    
    # Allocate memory for vertices and colors
    vertices_size = num_points * 3
    colors_size = num_points * 4
    
    # Initialize arrays
    vertices = [0.0] * vertices_size
    colors = [0] * colors_size

    # https://en.wikipedia.org/wiki/Spherical_coordinate_system
    for i in range(num_points):
        theta = math.pi * random.random()
        phi = 2.0 * math.pi * random.random()
        r = 10.0 * random.random()
        
        vertices[i*3 + 0] = r * math.sin(theta) * math.cos(phi)
        vertices[i*3 + 1] = r * math.sin(theta) * math.sin(phi)
        vertices[i*3 + 2] = r * math.cos(theta)
        
        color = rl.color_from_hsv(r * 360.0, 1.0, 1.0)
        
        colors[i*4 + 0] = color.r
        colors[i*4 + 1] = color.g
        colors[i*4 + 2] = color.b
        colors[i*4 + 3] = color.a
    
    # Assign data to mesh
    mesh.vertices = vertices
    mesh.colors = colors
    
    # Upload mesh data from CPU (RAM) to GPU (VRAM) memory
    rl.upload_mesh(mesh, False)
    
    return mesh

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raylib [models] example - point rendering")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(3.0, 3.0, 3.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    position = rl.Vector3(0.0, 0.0, 0.0)
    use_draw_model_points = True
    num_points_changed = False
    num_points = 1000
    
    mesh = gen_mesh_points(num_points)
    model = rl.load_model_from_mesh(mesh)
    
    # rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)

        if rl.is_key_pressed(rl.KEY_SPACE):
            use_draw_model_points = not use_draw_model_points
            
        if rl.is_key_pressed(rl.KEY_UP):
            num_points = min(num_points*10, MAX_POINTS)
            num_points_changed = True
            
        if rl.is_key_pressed(rl.KEY_DOWN):
            num_points = max(num_points//10, MIN_POINTS)
            num_points_changed = True

        # Upload a different point cloud size
        if num_points_changed:
            rl.unload_model(model)
            mesh = gen_mesh_points(num_points)
            model = rl.load_model_from_mesh(mesh)
            num_points_changed = False
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.begin_mode_3d(camera)

        # The new method only uploads the points once to the GPU
        if use_draw_model_points:
            rl.draw_model_points(model, position, 1.0, rl.WHITE)
        else:
            # The old method must continually draw the "points" (lines)
            for i in range(num_points):
                pos = rl.Vector3(
                    mesh.vertices[i*3 + 0],
                    mesh.vertices[i*3 + 1],
                    mesh.vertices[i*3 + 2]
                )
                color = rl.Color(
                    mesh.colors[i*4 + 0],
                    mesh.colors[i*4 + 1],
                    mesh.colors[i*4 + 2],
                    mesh.colors[i*4 + 3]
                )
                
                rl.draw_point_3d(pos, color)

        # Draw a unit sphere for reference
        rl.draw_sphere_wires(position, 1.0, 10, 10, rl.YELLOW)
            
        rl.end_mode_3d()

        # Draw UI text
        rl.draw_text(f"Point Count: {num_points}", 20, screen_height - 50, 40, rl.WHITE)
        rl.draw_text("Up - increase points", 20, 70, 20, rl.WHITE)
        rl.draw_text("Down - decrease points", 20, 100, 20, rl.WHITE)
        rl.draw_text("Space - drawing function", 20, 130, 20, rl.WHITE)
        
        if use_draw_model_points:
            rl.draw_text("Using: DrawModelPoints()", 20, 160, 20, rl.GREEN)
        else:
            rl.draw_text("Using: DrawPoint3D()", 20, 160, 20, rl.RED)
        
        rl.draw_fps(10, 10)
            
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model)

    rl.close_window()
    #--------------------------------------------------------------------------------------
