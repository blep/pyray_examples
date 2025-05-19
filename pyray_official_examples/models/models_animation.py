"""raylib [models] example - Load 3d model with animations and play them
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 3.5
Example contributed by Culacant (@culacant) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Culacant (@culacant) and Ramon Santamaria (@raysan5)
NOTE: To export a model from blender, make sure it is not posed, the vertices need to be 
      in the same position as they would be in edit mode and the scale of your models is 
      set to 0. Scaling can be done from the export menu.

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

    rl.init_window(screen_width, screen_height, "raylib [models] example - model animation")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(10.0, 10.0, 10.0)  # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)       # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 45.0                              # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE       # Camera mode type

    model = rl.load_model(str(THIS_DIR/"resources/models/iqm/guy.iqm"))           # Load the animated model mesh and basic data
    texture = rl.load_texture(str(THIS_DIR/"resources/models/iqm/guytex.png"))    # Load model texture and set material
    rl.set_material_texture(model.materials[0], rl.MATERIAL_MAP_DIFFUSE, texture) # Set model material map texture

    position = rl.Vector3(0.0, 0.0, 0.0)            # Set model position

    # Load animation data
    anims_count = rl.ffi.new("int *")
    anims = rl.load_model_animations(str(THIS_DIR/"resources/models/iqm/guyanim.iqm"), anims_count)
    anim_frame_counter = 0

    rl.disable_cursor()                    # Catch cursor
    rl.set_target_fps(60)                  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        # Play animation when spacebar is held down
        if rl.is_key_down(rl.KEY_SPACE):
            anim_frame_counter += 1
            rl.update_model_animation(model, anims[0], anim_frame_counter)
            if anim_frame_counter >= anims[0].frameCount:
                anim_frame_counter = 0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_model_ex(model, position, rl.Vector3(1.0, 0.0, 0.0), -90.0, rl.Vector3(1.0, 1.0, 1.0), rl.WHITE)

        for i in range(model.boneCount):
            rl.draw_cube(anims[0].framePoses[anim_frame_counter][i].translation, 0.2, 0.2, 0.2, rl.RED)

        rl.draw_grid(10, 1.0)         # Draw a grid

        rl.end_mode_3d()

        rl.draw_text("PRESS SPACE to PLAY MODEL ANIMATION", 10, 10, 20, rl.MAROON)
        rl.draw_text("(c) Guy IQM 3D model by @culacant", screen_width - 200, screen_height - 20, 10, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture)                     # Unload texture
    rl.unload_model_animations(anims, anims_count[0])   # Unload model animations data
    rl.unload_model(model)                         # Unload model

    rl.close_window()                  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
