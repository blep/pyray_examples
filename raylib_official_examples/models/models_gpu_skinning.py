"""raylib [core] example - Doing skinning on the gpu using a vertex shader
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by Daniel Holden (@orangeduck) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 Daniel Holden (@orangeduck)
Note: Due to limitations in the Apple OpenGL driver, this feature does not work on MacOS

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import platform
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Define GLSL version based on platform
if platform.system() == 'Windows' or platform.system() == 'Linux':
    GLSL_VERSION = 330
else:  # Android or Web
    GLSL_VERSION = 100

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - GPU skinning")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(5.0, 5.0, 5.0)  # Camera position
    camera.target = rl.Vector3(0.0, 2.0, 0.0)    # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)        # Camera up vector (rotation towards target)
    camera.fovy = 45.0                          # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE    # Camera projection type

    # Load gltf model
    character_model = rl.load_model(str(THIS_DIR/"resources/models/gltf/greenman.glb"))  # Load character model
    
    # Load skinning shader
    skinning_shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/skinning.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/skinning.fs")
    )
    
    character_model.materials[1].shader = skinning_shader
    
    # Load gltf model animations
    anims_count = rl.ffi.new("int *", 0)
    anim_index = 0
    anim_current_frame = 0
    model_animations = rl.load_model_animations(str(THIS_DIR/"resources/models/gltf/greenman.glb"), anims_count)
    anims_count = anims_count[0]  # Dereference to get the count

    position = rl.Vector3(0.0, 0.0, 0.0)  # Set model position

    rl.disable_cursor()                  # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_THIRD_PERSON)
        
        # Select current animation
        if rl.is_key_pressed(rl.KEY_T):
            anim_index = (anim_index + 1) % anims_count
        elif rl.is_key_pressed(rl.KEY_G):
            anim_index = (anim_index + anims_count - 1) % anims_count

        # Update model animation
        anim = model_animations[anim_index]
        anim_current_frame = (anim_current_frame + 1) % anim.frameCount
        character_model.transform = rl.matrix_translate(position.x, position.y, position.z)
        rl.update_model_animation_bones(character_model, anim, anim_current_frame)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
        
        # Draw character mesh, pose calculation is done in shader (GPU skinning)
        rl.draw_mesh(character_model.meshes[0], character_model.materials[1], character_model.transform)

        rl.draw_grid(10, 1.0)
            
        rl.end_mode_3d()

        rl.draw_text("Use the T/G to switch animation", 10, 10, 20, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model_animations(model_animations, anims_count) # Unload model animation
    rl.unload_model(character_model)    # Unload model and meshes/material
    rl.unload_shader(skinning_shader)   # Unload GPU skinning shader
    
    rl.close_window()                  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
