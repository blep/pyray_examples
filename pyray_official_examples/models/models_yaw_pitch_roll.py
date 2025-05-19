"""raylib [models] example - Plane rotations (yaw, pitch, roll)
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.8, last time updated with raylib 4.0
Example contributed by Berni (@Berni8k) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Berni (@Berni8k) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    # SetConfigFlags(FLAG_MSAA_4X_HINT | FLAG_WINDOW_HIGHDPI);
    rl.init_window(screen_width, screen_height, "raylib [models] example - plane rotations (yaw, pitch, roll)")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 50.0, -120.0)  # Camera position perspective
    camera.target = rl.Vector3(0.0, 0.0, 0.0)        # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)            # Camera up vector (rotation towards target)
    camera.fovy = 30.0                               # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE        # Camera type

    model = rl.load_model(str(THIS_DIR/"resources/models/obj/plane.obj"))                  # Load model
    texture = rl.load_texture(str(THIS_DIR/"resources/models/obj/plane_diffuse.png"))      # Load model texture
    rl.set_material_texture(model.materials[0], rl.MATERIAL_MAP_DIFFUSE, texture)          # Set map diffuse texture

    pitch = 0.0
    roll = 0.0
    yaw = 0.0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Plane pitch (x-axis) controls
        if rl.is_key_down(rl.KEY_DOWN):
            pitch += 0.6
        elif rl.is_key_down(rl.KEY_UP):
            pitch -= 0.6
        else:
            if pitch > 0.3:
                pitch -= 0.3
            elif pitch < -0.3:
                pitch += 0.3

        # Plane yaw (y-axis) controls
        if rl.is_key_down(rl.KEY_S):
            yaw -= 1.0
        elif rl.is_key_down(rl.KEY_A):
            yaw += 1.0
        else:
            if yaw > 0.0:
                yaw -= 0.5
            elif yaw < 0.0:
                yaw += 0.5

        # Plane roll (z-axis) controls
        if rl.is_key_down(rl.KEY_LEFT):
            roll -= 1.0
        elif rl.is_key_down(rl.KEY_RIGHT):
            roll += 1.0
        else:
            if roll > 0.0:
                roll -= 0.5
            elif roll < 0.0:
                roll += 0.5

        # Tranformation matrix for rotations
        model.transform = rl.matrix_rotate_xyz(rl.Vector3(math.radians(pitch), math.radians(yaw), math.radians(roll)))
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        # Draw 3D model (recomended to draw 3D always before 2D)
        rl.begin_mode_3d(camera)

        rl.draw_model(model, rl.Vector3(0.0, -8.0, 0.0), 1.0, rl.WHITE)   # Draw 3d model with texture
        rl.draw_grid(10, 10.0)

        rl.end_mode_3d()

        # Draw controls info
        rl.draw_rectangle(30, 370, 260, 70, rl.fade(rl.GREEN, 0.5))
        rl.draw_rectangle_lines(30, 370, 260, 70, rl.fade(rl.DARKGREEN, 0.5))
        rl.draw_text("Pitch controlled with: KEY_UP / KEY_DOWN", 40, 380, 10, rl.DARKGRAY)
        rl.draw_text("Roll controlled with: KEY_LEFT / KEY_RIGHT", 40, 400, 10, rl.DARKGRAY)
        rl.draw_text("Yaw controlled with: KEY_A / KEY_S", 40, 420, 10, rl.DARKGRAY)

        rl.draw_text("(c) WWI Plane Model created by GiaHanLam", screen_width - 240, screen_height - 20, 10, rl.DARKGRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model)     # Unload model data
    rl.unload_texture(texture) # Unload texture data

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
