"""raylib [models] example - Waving cubes
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 2.5, last time updated with raylib 3.7
Example contributed by Codecat (@codecat) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Codecat (@codecat) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Program main entry point
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - waving cubes")

    # Initialize the camera
    camera = rl.Camera3D()
    camera.position = rl.Vector3(30.0, 20.0, 30.0)  # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)       # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 70.0                              # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE       # Camera projection type

    # Specify the amount of blocks in each direction
    num_blocks = 15

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        time = rl.get_time()

        # Calculate time scale for cube position and size
        scale = (2.0 + math.sin(time)) * 0.7

        # Move camera around the scene
        camera_time = time * 0.3
        camera.position.x = math.cos(camera_time) * 40.0
        camera.position.z = math.sin(camera_time) * 40.0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_grid(10, 5.0)

        for x in range(num_blocks):
            for y in range(num_blocks):
                for z in range(num_blocks):
                    # Scale of the blocks depends on x/y/z positions
                    block_scale = (x + y + z) / 30.0

                    # Scatter makes the waving effect by adding block_scale over time
                    scatter = math.sin(block_scale * 20.0 + (time * 4.0))

                    # Calculate the cube position
                    cube_pos = rl.Vector3(
                        (x - num_blocks/2) * (scale * 3.0) + scatter,
                        (y - num_blocks/2) * (scale * 2.0) + scatter,
                        (z - num_blocks/2) * (scale * 3.0) + scatter
                    )

                    # Pick a color with a hue depending on cube position for the rainbow color effect
                    # NOTE: This function is quite costly to be done per cube and frame,
                    # pre-catching the results into a separate array could improve performance
                    cube_color = rl.color_from_hsv(((x + y + z) * 18) % 360, 0.75, 0.9)

                    # Calculate cube size
                    cube_size = (2.4 - scale) * block_scale

                    # And finally, draw the cube!
                    rl.draw_cube(cube_pos, cube_size, cube_size, cube_size, cube_color)

        rl.end_mode_3d()

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
