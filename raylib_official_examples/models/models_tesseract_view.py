"""raylib [models] example - Tesseract view
NOTE: This example only works on platforms that support drag & drop (Windows, Linux, OSX, Html5?)
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 5.6-dev, last time updated with raylib 5.6-dev
Example contributed by Timothy van der Valk (@arceryz) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 Timothy van der Valk (@arceryz) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Define Vector4 class since it's not available in pyray
class Vector4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def __eq__(self, other):
        if not isinstance(other, Vector4):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - tesseract view")
    
    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(4.0, 4.0, 4.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 0.0, 1.0)          # Camera up vector (rotation towards target)
    camera.fovy = 50.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera mode type

    # Find the coordinates by setting XYZW to +-1
    tesseract = [
        Vector4( 1,  1,  1, 1), Vector4( 1,  1,  1, -1),
        Vector4( 1,  1, -1, 1), Vector4( 1,  1, -1, -1),
        Vector4( 1, -1,  1, 1), Vector4( 1, -1,  1, -1),
        Vector4( 1, -1, -1, 1), Vector4( 1, -1, -1, -1),
        Vector4(-1,  1,  1, 1), Vector4(-1,  1,  1, -1),
        Vector4(-1,  1, -1, 1), Vector4(-1,  1, -1, -1),
        Vector4(-1, -1,  1, 1), Vector4(-1, -1,  1, -1),
        Vector4(-1, -1, -1, 1), Vector4(-1, -1, -1, -1),
    ]
    
    rotation = 0.0
    transformed = [rl.Vector3(0, 0, 0) for _ in range(16)]
    w_values = [0.0] * 16

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rotation = math.radians(45.0) * rl.get_time()
        
        for i in range(16):
            p = tesseract[i]

            # Rotate the XW part of the vector
            rot_xw = rl.vector2_rotate(rl.Vector2(p.x, p.w), rotation)
            p.x = rot_xw.x
            p.w = rot_xw.y

            # Projection from XYZW to XYZ from perspective point (0, 0, 0, 3)
            # NOTE: Trace a ray from (0, 0, 0, 3) > p and continue until W = 0
            c = 3.0/(3.0 - p.w)
            p.x = c * p.x
            p.y = c * p.y
            p.z = c * p.z

            # Split XYZ coordinate and W values later for drawing
            transformed[i] = rl.Vector3(p.x, p.y, p.z)
            w_values[i] = p.w
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        rl.begin_mode_3d(camera)
        for i in range(16):
            # Draw spheres to indicate the W value
            rl.draw_sphere(transformed[i], abs(w_values[i]*0.1), rl.RED)

            for j in range(16):
                # Two lines are connected if they differ by 1 coordinate
                # This way we dont have to keep an edge list
                v1 = tesseract[i]
                v2 = tesseract[j]
                diff = int(v1.x == v2.x) + int(v1.y == v2.y) + int(v1.z == v2.z) + int(v1.w == v2.w)

                # Draw only differing by 1 coordinate and the lower index only (duplicate lines)
                if diff == 3 and i < j:
                    rl.draw_line_3d(transformed[i], transformed[j], rl.MAROON)
        rl.end_mode_3d()
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
