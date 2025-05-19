"""raylib [models] example - Load models M3D
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by bzt (@bztsrc) and reviewed by Ramon Santamaria (@raysan5)
NOTES:
  - Model3D (M3D) fileformat specs: https://gitlab.com/bztsrc/model3d
  - Bender M3D exported: https://gitlab.com/bztsrc/model3d/-/tree/master/blender
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 bzt (@bztsrc)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import os
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

    rl.init_window(screen_width, screen_height, "raylib [models] example - M3D model loading")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(1.5, 1.5, 1.5)    # Camera position
    camera.target = rl.Vector3(0.0, 0.4, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    position = rl.Vector3(0.0, 0.0, 0.0)           # Set model position

    model_file_name = str(THIS_DIR/"resources/models/m3d/cesium_man.m3d")
    draw_mesh = True
    draw_skeleton = True
    anim_playing = False   # Store anim state, what to draw

    # Load model
    model = rl.load_model(model_file_name)  # Load the bind-pose model mesh and basic data

    # Load animations
    anims_count = rl.ffi.new("int *", 0)
    anim_frame_counter = 0
    anim_id = 0
    anims = rl.load_model_animations(model_file_name, anims_count)  # Load skeletal animation data
    anims_count = anims_count[0]  # Dereference to get the count

    rl.disable_cursor()                  # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():     # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        if anims_count:
            # Play animation when spacebar is held down (or step one frame with N)
            if rl.is_key_down(rl.KEY_SPACE) or rl.is_key_pressed(rl.KEY_N):
                anim_frame_counter += 1

                if anim_frame_counter >= anims[anim_id].frameCount:
                    anim_frame_counter = 0

                rl.update_model_animation(model, anims[anim_id], anim_frame_counter)
                anim_playing = True

            # Select animation by pressing C
            if rl.is_key_pressed(rl.KEY_C):
                anim_frame_counter = 0
                anim_id += 1

                if anim_id >= anims_count:
                    anim_id = 0
                rl.update_model_animation(model, anims[anim_id], 0)
                anim_playing = True

        # Toggle skeleton drawing
        if rl.is_key_pressed(rl.KEY_B):
            draw_skeleton = not draw_skeleton

        # Toggle mesh drawing
        if rl.is_key_pressed(rl.KEY_M):
            draw_mesh = not draw_mesh
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        # Draw 3d model with texture
        if draw_mesh:
            rl.draw_model(model, position, 1.0, rl.WHITE)

        # Draw the animated skeleton
        if draw_skeleton:
            # Loop to (boneCount - 1) because the last one is a special "no bone" bone,
            # needed to workaround buggy models
            # without a -1, we would always draw a cube at the origin
            for i in range(model.boneCount - 1):
                # By default the model is loaded in bind-pose by LoadModel().
                # But if UpdateModelAnimation() has been called at least once
                # then the model is already in animation pose, so we need the animated skeleton
                if not anim_playing or not anims_count:
                    # Display the bind-pose skeleton
                    rl.draw_cube(model.bindPose[i].translation, 0.04, 0.04, 0.04, rl.RED)

                    if model.bones[i].parent >= 0:
                        rl.draw_line_3d(
                            model.bindPose[i].translation,
                            model.bindPose[model.bones[i].parent].translation,
                            rl.RED
                        )
                else:
                    # Display the frame-pose skeleton
                    rl.draw_cube(
                        anims[anim_id].framePoses[anim_frame_counter][i].translation,
                        0.05, 0.05, 0.05,
                        rl.RED
                    )

                    if anims[anim_id].bones[i].parent >= 0:
                        rl.draw_line_3d(
                            anims[anim_id].framePoses[anim_frame_counter][i].translation,
                            anims[anim_id].framePoses[anim_frame_counter][anims[anim_id].bones[i].parent].translation,
                            rl.RED
                        )

        rl.draw_grid(10, 1.0)         # Draw a grid

        rl.end_mode_3d()

        rl.draw_text("PRESS SPACE to PLAY MODEL ANIMATION", 10, rl.get_screen_height() - 80, 10, rl.MAROON)
        rl.draw_text("PRESS N to STEP ONE ANIMATION FRAME", 10, rl.get_screen_height() - 60, 10, rl.DARKGRAY)
        rl.draw_text("PRESS C to CYCLE THROUGH ANIMATIONS", 10, rl.get_screen_height() - 40, 10, rl.DARKGRAY)
        rl.draw_text("PRESS M to toggle MESH, B to toggle SKELETON DRAWING", 10, rl.get_screen_height() - 20, 10, rl.DARKGRAY)
        rl.draw_text("(c) CesiumMan model by KhronosGroup", rl.get_screen_width() - 210, rl.get_screen_height() - 20, 10, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    # Unload model animations data
    rl.unload_model_animations(anims, anims_count)

    rl.unload_model(model)         # Unload model

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
