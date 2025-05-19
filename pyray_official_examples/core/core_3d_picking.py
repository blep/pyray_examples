"""raylib [core] example - Picking in 3d mode
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.3, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - 3d picking")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(10.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    cube_position = rl.Vector3(0.0, 1.0, 0.0)
    cube_size = rl.Vector3(2.0, 2.0, 2.0)

    ray = rl.Ray() # Initialize Ray
    collision = rl.RayCollision() # Initialize RayCollision
    collision.hit = False # Explicitly set hit to False initially

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        if rl.is_cursor_hidden():
            rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
            if rl.is_cursor_hidden():
                rl.enable_cursor()
            else:
                rl.disable_cursor()

        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            # Before C version checked !collision.hit, but Python needs to handle the case where collision is None or not yet defined
            # For simplicity, we always get the ray and check collision.
            # If it was already hit, this effectively deselects and re-evaluates.
            ray = rl.get_screen_to_world_ray(rl.get_mouse_position(), camera)
            
            bounding_box = rl.BoundingBox(
                rl.Vector3(cube_position.x - cube_size.x / 2, cube_position.y - cube_size.y / 2, cube_position.z - cube_size.z / 2),
                rl.Vector3(cube_position.x + cube_size.x / 2, cube_position.y + cube_size.y / 2, cube_position.z + cube_size.z / 2)
            )
            collision = rl.get_ray_collision_box(ray, bounding_box)
        
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        if collision.hit:
            rl.draw_cube(cube_position, cube_size.x, cube_size.y, cube_size.z, rl.RED)
            rl.draw_cube_wires(cube_position, cube_size.x, cube_size.y, cube_size.z, rl.MAROON)
            rl.draw_cube_wires(cube_position, cube_size.x + 0.2, cube_size.y + 0.2, cube_size.z + 0.2, rl.GREEN)
        else:
            rl.draw_cube(cube_position, cube_size.x, cube_size.y, cube_size.z, rl.GRAY)
            rl.draw_cube_wires(cube_position, cube_size.x, cube_size.y, cube_size.z, rl.DARKGRAY)

        rl.draw_ray(ray, rl.MAROON)
        rl.draw_grid(10, 1.0)

        rl.end_mode_3d()

        rl.draw_text("Try clicking on the box with your mouse!", 240, 10, 20, rl.DARKGRAY)

        if collision.hit:
            text = "BOX SELECTED"
            text_width = rl.measure_text(text, 30)
            rl.draw_text(text, (screen_width - text_width) // 2, int(screen_height * 0.1), 30, rl.GREEN)

        rl.draw_text("Right click mouse to toggle camera controls", 10, 430, 10, rl.GRAY)
        rl.draw_fps(10, 10)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
