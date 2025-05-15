"""raylib [models] example - Drawing billboards
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 1.3, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib [models] example - drawing billboards")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(5.0, 4.0, 5.0)       # Camera position
    camera.target = rl.Vector3(0.0, 2.0, 0.0)         # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)             # Camera up vector (rotation towards target)
    camera.fovy = 45.0                                # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE         # Camera projection type

    bill = rl.load_texture(str(THIS_DIR/"resources/billboard.png"))    # Our billboard texture
    bill_position_static = rl.Vector3(0.0, 2.0, 0.0)           # Position of static billboard
    bill_position_rotating = rl.Vector3(1.0, 2.0, 1.0)         # Position of rotating billboard

    # Entire billboard texture, source is used to take a segment from a larger texture.
    source = rl.Rectangle(0.0, 0.0, float(bill.width), float(bill.height))

    # NOTE: Billboard locked on axis-Y
    bill_up = rl.Vector3(0.0, 1.0, 0.0)

    # Set the height of the rotating billboard to 1.0 with the aspect ratio fixed
    size = rl.Vector2(source.width/source.height, 1.0)

    # Rotate around origin
    # Here we choose to rotate around the image center
    origin = rl.vector2_scale(size, 0.5)

    # Distance is needed for the correct billboard draw order
    # Larger distance (further away from the camera) should be drawn prior to smaller distance.
    distance_static = 0.0
    distance_rotating = 0.0
    rotation = 0.0

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)

        rotation += 0.4
        distance_static = rl.vector3_distance(camera.position, bill_position_static)
        distance_rotating = rl.vector3_distance(camera.position, bill_position_rotating)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_grid(10, 1.0)        # Draw a grid

        # Draw order matters!
        if distance_static > distance_rotating:
            rl.draw_billboard(camera, bill, bill_position_static, 2.0, rl.WHITE)
            rl.draw_billboard_pro(camera, bill, source, bill_position_rotating, bill_up, size, origin, rotation, rl.WHITE)
        else:
            rl.draw_billboard_pro(camera, bill, source, bill_position_rotating, bill_up, size, origin, rotation, rl.WHITE)
            rl.draw_billboard(camera, bill, bill_position_static, 2.0, rl.WHITE)

        rl.end_mode_3d()

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(bill)        # Unload texture

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
