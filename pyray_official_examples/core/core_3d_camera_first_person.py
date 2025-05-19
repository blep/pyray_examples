"""raylib [core] example - 3d camera first person
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random
import math

MAX_COLUMNS = 20

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - 3d camera first person")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 2.0, 4.0)
    camera.target = rl.Vector3(0.0, 2.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 60.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    # Initialize camera mode after camera struct is defined
    camera_mode = rl.CAMERA_FIRST_PERSON 

    heights = [0.0] * MAX_COLUMNS
    positions = [rl.Vector3() for _ in range(MAX_COLUMNS)]
    colors = [rl.Color() for _ in range(MAX_COLUMNS)]

    for i in range(MAX_COLUMNS):
        heights[i] = float(rl.get_random_value(1, 12))
        positions[i] = rl.Vector3(float(rl.get_random_value(-15, 15)), heights[i] / 2.0, float(rl.get_random_value(-15, 15)))
        colors[i] = rl.Color(rl.get_random_value(20, 255), rl.get_random_value(10, 55), 30, 255)

    rl.disable_cursor()
    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        if rl.is_key_pressed(rl.KEY_ONE):
            camera_mode = rl.CAMERA_FREE
            camera.up = rl.Vector3(0.0, 1.0, 0.0)
        if rl.is_key_pressed(rl.KEY_TWO):
            camera_mode = rl.CAMERA_FIRST_PERSON
            camera.up = rl.Vector3(0.0, 1.0, 0.0)
        if rl.is_key_pressed(rl.KEY_THREE):
            camera_mode = rl.CAMERA_THIRD_PERSON
            camera.up = rl.Vector3(0.0, 1.0, 0.0)
        if rl.is_key_pressed(rl.KEY_FOUR):
            camera_mode = rl.CAMERA_ORBITAL
            camera.up = rl.Vector3(0.0, 1.0, 0.0)

        if rl.is_key_pressed(rl.KEY_P):
            if camera.projection == rl.CAMERA_PERSPECTIVE:
                camera_mode = rl.CAMERA_THIRD_PERSON # Ensure camera mode is updated before changing projection params
                camera.position = rl.Vector3(0.0, 2.0, -100.0)
                camera.target = rl.Vector3(0.0, 2.0, 0.0)
                camera.up = rl.Vector3(0.0, 1.0, 0.0)
                camera.projection = rl.CAMERA_ORTHOGRAPHIC
                camera.fovy = 20.0
                # Corrected: Pass camera by reference (as it's a class instance, it's already a reference)
                # In Python, objects are passed by assignment (reference), so direct modification works.
                # The C functions CameraYaw and CameraPitch modify the camera struct directly.
                # The pyray bindings for these likely expect the camera object itself.
                rl.camera_yaw(camera, -135 * rl.DEG2RAD, True)
                rl.camera_pitch(camera, -45 * rl.DEG2RAD, True, True, False)
            elif camera.projection == rl.CAMERA_ORTHOGRAPHIC:
                camera_mode = rl.CAMERA_THIRD_PERSON # Ensure camera mode is updated
                camera.position = rl.Vector3(0.0, 2.0, 10.0)
                camera.target = rl.Vector3(0.0, 2.0, 0.0)
                camera.up = rl.Vector3(0.0, 1.0, 0.0)
                camera.projection = rl.CAMERA_PERSPECTIVE
                camera.fovy = 60.0
        
        # Corrected: Pass camera by reference for update_camera
        rl.update_camera(camera, camera_mode)

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        rl.begin_mode_3d(camera)

        rl.draw_plane(rl.Vector3(0.0, 0.0, 0.0), rl.Vector2(32.0, 32.0), rl.LIGHTGRAY)
        rl.draw_cube(rl.Vector3(-16.0, 2.5, 0.0), 1.0, 5.0, 32.0, rl.BLUE)
        rl.draw_cube(rl.Vector3(16.0, 2.5, 0.0), 1.0, 5.0, 32.0, rl.LIME)
        rl.draw_cube(rl.Vector3(0.0, 2.5, 16.0), 32.0, 5.0, 1.0, rl.GOLD)

        for i in range(MAX_COLUMNS):
            rl.draw_cube(positions[i], 2.0, heights[i], 2.0, colors[i])
            rl.draw_cube_wires(positions[i], 2.0, heights[i], 2.0, rl.MAROON)

        if camera_mode == rl.CAMERA_THIRD_PERSON:
            rl.draw_cube(camera.target, 0.5, 0.5, 0.5, rl.PURPLE)
            rl.draw_cube_wires(camera.target, 0.5, 0.5, 0.5, rl.DARKPURPLE)

        rl.end_mode_3d()

        rl.draw_rectangle(5, 5, 330, 100, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(5, 5, 330, 100, rl.BLUE)
        rl.draw_text("Camera controls:", 15, 15, 10, rl.BLACK)
        rl.draw_text("- Move keys: W, A, S, D, Space, Left-Ctrl", 15, 30, 10, rl.BLACK)
        rl.draw_text("- Look around: arrow keys or mouse", 15, 45, 10, rl.BLACK)
        rl.draw_text("- Camera mode keys: 1, 2, 3, 4", 15, 60, 10, rl.BLACK)
        rl.draw_text("- Zoom keys: num-plus, num-minus or mouse scroll", 15, 75, 10, rl.BLACK)
        rl.draw_text("- Camera projection key: P", 15, 90, 10, rl.BLACK)

        rl.draw_rectangle(600, 5, 195, 100, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(600, 5, 195, 100, rl.BLUE)
        rl.draw_text("Camera status:", 610, 15, 10, rl.BLACK)
        
        mode_text = ""
        if camera_mode == rl.CAMERA_FREE: mode_text = "FREE"
        elif camera_mode == rl.CAMERA_FIRST_PERSON: mode_text = "FIRST_PERSON"
        elif camera_mode == rl.CAMERA_THIRD_PERSON: mode_text = "THIRD_PERSON"
        elif camera_mode == rl.CAMERA_ORBITAL: mode_text = "ORBITAL"
        else: mode_text = "CUSTOM"
        rl.draw_text(f"- Mode: {mode_text}", 610, 30, 10, rl.BLACK)

        proj_text = ""
        if camera.projection == rl.CAMERA_PERSPECTIVE: proj_text = "PERSPECTIVE"
        elif camera.projection == rl.CAMERA_ORTHOGRAPHIC: proj_text = "ORTHOGRAPHIC"
        else: proj_text = "CUSTOM"
        rl.draw_text(f"- Projection: {proj_text}", 610, 45, 10, rl.BLACK)

        rl.draw_text(f"- Position: ({camera.position.x:.3f}, {camera.position.y:.3f}, {camera.position.z:.3f})", 610, 60, 10, rl.BLACK)
        rl.draw_text(f"- Target: ({camera.target.x:.3f}, {camera.target.y:.3f}, {camera.target.z:.3f})", 610, 75, 10, rl.BLACK)
        rl.draw_text(f"- Up: ({camera.up.x:.3f}, {camera.up.y:.3f}, {camera.up.z:.3f})", 610, 90, 10, rl.BLACK)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
