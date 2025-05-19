"""raylib [core] example - Initialize 3d camera mode
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.0, last time updated with raylib 1.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - 3d camera mode")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    cube_position = rl.Vector3(0.0, 0.0, 0.0)

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        # No update logic in this example

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_cube(cube_position, 2.0, 2.0, 2.0, rl.RED)
        rl.draw_cube_wires(cube_position, 2.0, 2.0, 2.0, rl.MAROON)
        rl.draw_grid(10, 1.0)

        rl.end_mode_3d()

        rl.draw_text("Welcome to the third dimension!", 10, 40, 20, rl.DARKGRAY)
        rl.draw_fps(10, 10)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
