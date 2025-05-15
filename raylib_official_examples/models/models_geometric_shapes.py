"""raylib [models] example - Draw some basic geometric shapes (cube, sphere, cylinder...)
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.0, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Program main entry point
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - geometric shapes")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # TODO: Update your variables here
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_cube(rl.Vector3(-4.0, 0.0, 2.0), 2.0, 5.0, 2.0, rl.RED)
        rl.draw_cube_wires(rl.Vector3(-4.0, 0.0, 2.0), 2.0, 5.0, 2.0, rl.GOLD)
        rl.draw_cube_wires(rl.Vector3(-4.0, 0.0, -2.0), 3.0, 6.0, 2.0, rl.MAROON)

        rl.draw_sphere(rl.Vector3(-1.0, 0.0, -2.0), 1.0, rl.GREEN)
        rl.draw_sphere_wires(rl.Vector3(1.0, 0.0, 2.0), 2.0, 16, 16, rl.LIME)

        rl.draw_cylinder(rl.Vector3(4.0, 0.0, -2.0), 1.0, 2.0, 3.0, 4, rl.SKYBLUE)
        rl.draw_cylinder_wires(rl.Vector3(4.0, 0.0, -2.0), 1.0, 2.0, 3.0, 4, rl.DARKBLUE)
        rl.draw_cylinder_wires(rl.Vector3(4.5, -1.0, 2.0), 1.0, 1.0, 2.0, 6, rl.BROWN)

        rl.draw_cylinder(rl.Vector3(1.0, 0.0, -4.0), 0.0, 1.5, 3.0, 8, rl.GOLD)
        rl.draw_cylinder_wires(rl.Vector3(1.0, 0.0, -4.0), 0.0, 1.5, 3.0, 8, rl.PINK)

        rl.draw_capsule(rl.Vector3(-3.0, 1.5, -4.0), rl.Vector3(-4.0, -1.0, -4.0), 1.2, 8, 8, rl.VIOLET)
        rl.draw_capsule_wires(rl.Vector3(-3.0, 1.5, -4.0), rl.Vector3(-4.0, -1.0, -4.0), 1.2, 8, 8, rl.PURPLE)

        rl.draw_grid(10, 1.0)        # Draw a grid

        rl.end_mode_3d()

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
