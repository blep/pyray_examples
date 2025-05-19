"""raylib [core] example - Using bones as socket for calculating the positioning of something
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by iP (@ipzaur) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 iP (@ipzaur)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Define constants
BONE_SOCKETS = 3
BONE_SOCKET_HAT = 0
BONE_SOCKET_HAND_R = 1
BONE_SOCKET_HAND_L = 2

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - bone socket")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(5.0, 5.0, 5.0)  # Camera position
    camera.target = rl.Vector3(0.0, 2.0, 0.0)    # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)        # Camera up vector (rotation towards target)
    camera.fovy = 45.0                          # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE    # Camera projection type

    # Load gltf model
    character_model = rl.load_model(str(THIS_DIR/"resources/models/gltf/greenman.glb"))  # Load character model
    equip_model = [None] * BONE_SOCKETS
    equip_model[0] = rl.load_model(str(THIS_DIR/"resources/models/gltf/greenman_hat.glb"))    # Index for the hat model is the same as BONE_SOCKET_HAT
    equip_model[1] = rl.load_model(str(THIS_DIR/"resources/models/gltf/greenman_sword.glb"))  # Index for the sword model is the same as BONE_SOCKET_HAND_R
    equip_model[2] = rl.load_model(str(THIS_DIR/"resources/models/gltf/greenman_shield.glb"))  # Index for the shield model is the same as BONE_SOCKET_HAND_L
    
    show_equip = [True, True, True]  # Toggle on/off equip

    # Load gltf model animations
    anims_count = rl.ffi.new("int *", 0)
    anim_index = 0
    anim_current_frame = 0
    model_animations = rl.load_model_animations(str(THIS_DIR/"resources/models/gltf/greenman.glb"), anims_count)
    anims_count = anims_count[0]  # Dereference to get the count

    # indices of bones for sockets
    bone_socket_index = [-1, -1, -1]

    # search bones for sockets 
    for i in range(character_model.boneCount):
        bone_name = rl.ffi.string(character_model.bones[i].name).decode('utf-8')
        
        if bone_name == "socket_hat":
            bone_socket_index[BONE_SOCKET_HAT] = i
            continue
        
        if bone_name == "socket_hand_R":
            bone_socket_index[BONE_SOCKET_HAND_R] = i
            continue
        
        if bone_name == "socket_hand_L":
            bone_socket_index[BONE_SOCKET_HAND_L] = i
            continue

    position = rl.Vector3(0.0, 0.0, 0.0)  # Set model position
    angle = 0                            # Set angle for rotate character

    rl.disable_cursor()                  # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_THIRD_PERSON)
        
        # Rotate character
        if rl.is_key_down(rl.KEY_F):
            angle = (angle + 1) % 360
        elif rl.is_key_down(rl.KEY_H):
            angle = (360 + angle - 1) % 360

        # Select current animation
        if rl.is_key_pressed(rl.KEY_T):
            anim_index = (anim_index + 1) % anims_count
        elif rl.is_key_pressed(rl.KEY_G):
            anim_index = (anim_index + anims_count - 1) % anims_count

        # Toggle shown of equip
        if rl.is_key_pressed(rl.KEY_ONE):
            show_equip[BONE_SOCKET_HAT] = not show_equip[BONE_SOCKET_HAT]
        if rl.is_key_pressed(rl.KEY_TWO):
            show_equip[BONE_SOCKET_HAND_R] = not show_equip[BONE_SOCKET_HAND_R]
        if rl.is_key_pressed(rl.KEY_THREE):
            show_equip[BONE_SOCKET_HAND_L] = not show_equip[BONE_SOCKET_HAND_L]
        
        # Update model animation
        anim = model_animations[anim_index]
        anim_current_frame = (anim_current_frame + 1) % anim.frameCount
        rl.update_model_animation(character_model, anim, anim_current_frame)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
            # Draw character
        character_rotate = rl.quaternion_from_axis_angle(rl.Vector3(0.0, 1.0, 0.0), angle * rl.DEG2RAD)
        character_model.transform = rl.matrix_multiply(
            rl.quaternion_to_matrix(character_rotate),
            rl.matrix_translate(position.x, position.y, position.z)
        )
        rl.update_model_animation(character_model, anim, anim_current_frame)
        rl.draw_mesh(character_model.meshes[0], character_model.materials[1], character_model.transform)

        # Draw equipments (hat, sword, shield)
        for i in range(BONE_SOCKETS):
            if not show_equip[i]:
                continue

            transform = anim.framePoses[anim_current_frame][bone_socket_index[i]]
            in_rotation = character_model.bindPose[bone_socket_index[i]].rotation
            out_rotation = transform.rotation
            
            # Calculate socket rotation (angle between bone in initial pose and same bone in current animation frame)
            rotate = rl.quaternion_multiply(out_rotation, rl.quaternion_invert(in_rotation))
            matrix_transform = rl.quaternion_to_matrix(rotate)
            # Translate socket to its position in the current animation
            matrix_transform = rl.matrix_multiply(
                matrix_transform,
                rl.matrix_translate(transform.translation.x, transform.translation.y, transform.translation.z)
            )
            # Transform the socket using the transform of the character (angle and translate)
            matrix_transform = rl.matrix_multiply(matrix_transform, character_model.transform)
            
            # Draw mesh at socket position with socket angle rotation
            rl.draw_mesh(equip_model[i].meshes[0], equip_model[i].materials[1], matrix_transform)

        rl.draw_grid(10, 1.0)
        rl.end_mode_3d()

        rl.draw_text("Use the T/G to switch animation", 10, 10, 20, rl.GRAY)
        rl.draw_text("Use the F/H to rotate character left/right", 10, 35, 20, rl.GRAY)
        rl.draw_text("Use the 1,2,3 to toggle shown of hat, sword and shield", 10, 60, 20, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model_animations(model_animations, anims_count)
    rl.unload_model(character_model)         # Unload character model and meshes/material
    
    # Unload equipment model and meshes/material
    for i in range(BONE_SOCKETS):
        rl.unload_model(equip_model[i])

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
