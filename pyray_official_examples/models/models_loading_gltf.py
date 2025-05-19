"""raylib [models] example - loading gltf with animations
Example complexity rating: [★☆☆☆] 1/4
LIMITATIONS:
  - Only supports 1 armature per file, and skips loading it if there are multiple armatures
  - Only supports linear interpolation (default method in Blender when checked
    "Always Sample Animations" when exporting a GLTF file)
  - Only supports translation/rotation/scale animation channel.path,
    weights not considered (i.e. morph targets)
Example originally created with raylib 3.7, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
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

    rl.init_window(screen_width, screen_height, "raylib [models] example - loading gltf animations")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(6.0, 6.0, 6.0)    # Camera position
    camera.target = rl.Vector3(0.0, 2.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load gltf model
    model = rl.load_model(str(THIS_DIR/"resources/models/gltf/robot.glb"))
    position = rl.Vector3(0.0, 0.0, 0.0)  # Set model position
    
    # Load gltf model animations
    anims_count = rl.ffi.new("int *", 0)
    anim_index = 0
    anim_current_frame = 0
    model_animations = rl.load_model_animations(str(THIS_DIR/"resources/models/gltf/robot.glb"), anims_count)
    anims_count = anims_count[0]  # Dereference to get the count

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)

        # Select current animation
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
            anim_index = (anim_index + 1) % anims_count
        elif rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            anim_index = (anim_index + anims_count - 1) % anims_count

        # Update model animation
        anim = model_animations[anim_index]
        anim_current_frame = (anim_current_frame + 1) % anim.frameCount
        rl.update_model_animation(model, anim, anim_current_frame)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
        rl.draw_model(model, position, 1.0, rl.WHITE)    # Draw animated model
        rl.draw_grid(10, 1.0)
        rl.end_mode_3d()

        rl.draw_text("Use the LEFT/RIGHT mouse buttons to switch animation", 10, 10, 20, rl.GRAY)
        rl.draw_text(f"Animation: {anim.name}", 10, rl.get_screen_height() - 20, 10, rl.DARKGRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model)         # Unload model and meshes/material

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
