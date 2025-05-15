"""raylib [core] example - Initialize 3d camera free
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - 3d camera free")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(10.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    cube_position = rl.Vector3(0.0, 0.0, 0.0)

    rl.disable_cursor() 
    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        rl.update_camera(camera, rl.CAMERA_FREE) 

        if rl.is_key_pressed(rl.KEY_Z):
            camera.target = rl.Vector3(0.0, 0.0, 0.0)
        
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_cube(cube_position, 2.0, 2.0, 2.0, rl.RED)
        rl.draw_cube_wires(cube_position, 2.0, 2.0, 2.0, rl.MAROON)
        rl.draw_grid(10, 1.0)

        rl.end_mode_3d()

        rl.draw_rectangle(10, 10, 320, 93, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(10, 10, 320, 93, rl.BLUE)

        rl.draw_text("Free camera default controls:", 20, 20, 10, rl.BLACK)
        rl.draw_text("- Mouse Wheel to Zoom in-out", 40, 40, 10, rl.DARKGRAY)
        rl.draw_text("- Mouse Wheel Pressed to Pan", 40, 60, 10, rl.DARKGRAY) # Corrected: C example says Alt + Mouse Wheel Pressed
        rl.draw_text("- Z to zoom to (0, 0, 0)", 40, 80, 10, rl.DARKGRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
