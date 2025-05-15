"""raylib [core] example - World to screen
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.3, last time updated with raylib 1.4
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - core world screen")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(10.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    cube_position = rl.Vector3(0.0, 0.0, 0.0)
    # cube_screen_position = rl.Vector2(0.0, 0.0) # Not strictly needed to initialize here

    rl.disable_cursor() # Limit cursor to relative movement inside the window
    rl.set_target_fps(60)

    while not rl.window_should_close():
        rl.update_camera(camera, rl.CAMERA_THIRD_PERSON) # CAMERA_THIRD_PERSON not ideal for this, CAMERA_FREE or ORBITAL would be better

        cube_screen_position = rl.get_world_to_screen(rl.Vector3(cube_position.x, cube_position.y + 2.5, cube_position.z), camera)

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
        rl.draw_cube(cube_position, 2.0, 2.0, 2.0, rl.RED)
        rl.draw_cube_wires(cube_position, 2.0, 2.0, 2.0, rl.MAROON)
        rl.draw_grid(10, 1.0)
        rl.end_mode_3d()

        rl.draw_text("Enemy: 100 / 100", int(cube_screen_position.x - rl.measure_text("Enemy: 100/100", 20)/2), int(cube_screen_position.y), 20, rl.BLACK)
        rl.draw_text(f"Cube position in screen space coordinates: [{int(cube_screen_position.x)}, {int(cube_screen_position.y)}]", 10, 10, 20, rl.LIME)
        rl.draw_text("Text 2d should be always on top of the cube", 10, 40, 20, rl.GRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
