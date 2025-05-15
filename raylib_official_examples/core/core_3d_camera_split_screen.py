"""raylib [core] example - 3d cmaera split screen
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 3.7, last time updated with raylib 4.0
Example contributed by Jeffery Myers (@JeffM2501) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Jeffery Myers (@JeffM2501)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math # Not strictly necessary for this example, but good practice if vector math might be added

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - 3d camera split screen")

    # Setup player 1 camera and screen
    camera_player1 = rl.Camera3D()
    camera_player1.fovy = 45.0
    camera_player1.up = rl.Vector3(0.0, 1.0, 0.0) # Y is up
    camera_player1.target = rl.Vector3(0.0, 1.0, 0.0)
    camera_player1.position = rl.Vector3(0.0, 1.0, -3.0) # Start a bit behind the target
    camera_player1.projection = rl.CAMERA_PERSPECTIVE

    screen_player1 = rl.load_render_texture(screen_width // 2, screen_height)

    # Setup player 2 camera and screen
    camera_player2 = rl.Camera3D()
    camera_player2.fovy = 45.0
    camera_player2.up = rl.Vector3(0.0, 1.0, 0.0) # Y is up
    camera_player2.target = rl.Vector3(0.0, 3.0, 0.0) # Looking at a higher point
    camera_player2.position = rl.Vector3(-3.0, 3.0, 0.0) # Start to the side and higher
    camera_player2.projection = rl.CAMERA_PERSPECTIVE

    screen_player2 = rl.load_render_texture(screen_width // 2, screen_height)

    # Flipped rectangle for drawing render textures
    split_screen_rect = rl.Rectangle(0, 0, float(screen_player1.texture.width), float(-screen_player1.texture.height))

    # Grid data
    count = 5
    spacing = 4.0 # Make it float for calculations

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        offset_this_frame = 10.0 * rl.get_frame_time()

        # Move Player1 (controls Z axis)
        if rl.is_key_down(rl.KEY_W):
            camera_player1.position.z += offset_this_frame
            camera_player1.target.z += offset_this_frame
        elif rl.is_key_down(rl.KEY_S):
            camera_player1.position.z -= offset_this_frame
            camera_player1.target.z -= offset_this_frame

        # Move Player2 (controls X axis)
        if rl.is_key_down(rl.KEY_UP):
            camera_player2.position.x += offset_this_frame
            camera_player2.target.x += offset_this_frame
        elif rl.is_key_down(rl.KEY_DOWN):
            camera_player2.position.x -= offset_this_frame
            camera_player2.target.x -= offset_this_frame

        # Draw Player1 view
        rl.begin_texture_mode(screen_player1)
        rl.clear_background(rl.SKYBLUE)
        rl.begin_mode_3d(camera_player1)

        rl.draw_plane(rl.Vector3(0, 0, 0), rl.Vector2(50, 50), rl.BEIGE)
        x_val = -count * spacing
        while x_val <= count * spacing:
            z_val = -count * spacing
            while z_val <= count * spacing:
                rl.draw_cube(rl.Vector3(x_val, 1.5, z_val), 1, 1, 1, rl.LIME)
                rl.draw_cube(rl.Vector3(x_val, 0.5, z_val), 0.25, 1, 0.25, rl.BROWN)
                z_val += spacing
            x_val += spacing

        rl.draw_cube(camera_player1.position, 1, 1, 1, rl.RED)
        rl.draw_cube(camera_player2.position, 1, 1, 1, rl.BLUE)

        rl.end_mode_3d()
        rl.draw_rectangle(0, 0, screen_width // 2, 40, rl.fade(rl.RAYWHITE, 0.8))
        rl.draw_text("PLAYER1: W/S to move", 10, 10, 20, rl.MAROON)
        rl.end_texture_mode()

        # Draw Player2 view
        rl.begin_texture_mode(screen_player2)
        rl.clear_background(rl.SKYBLUE)
        rl.begin_mode_3d(camera_player2)

        rl.draw_plane(rl.Vector3(0, 0, 0), rl.Vector2(50, 50), rl.BEIGE)
        x_val = -count * spacing
        while x_val <= count * spacing:
            z_val = -count * spacing
            while z_val <= count * spacing:
                rl.draw_cube(rl.Vector3(x_val, 1.5, z_val), 1, 1, 1, rl.LIME)
                rl.draw_cube(rl.Vector3(x_val, 0.5, z_val), 0.25, 1, 0.25, rl.BROWN)
                z_val += spacing
            x_val += spacing

        rl.draw_cube(camera_player1.position, 1, 1, 1, rl.RED)
        rl.draw_cube(camera_player2.position, 1, 1, 1, rl.BLUE)

        rl.end_mode_3d()
        rl.draw_rectangle(0, 0, screen_width // 2, 40, rl.fade(rl.RAYWHITE, 0.8))
        rl.draw_text("PLAYER2: UP/DOWN to move", 10, 10, 20, rl.DARKBLUE)
        rl.end_texture_mode()

        # Draw both views to screen
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_texture_rec(screen_player1.texture, split_screen_rect, rl.Vector2(0, 0), rl.WHITE)
        rl.draw_texture_rec(screen_player2.texture, split_screen_rect, rl.Vector2(screen_width / 2.0, 0), rl.WHITE)
        rl.draw_rectangle(screen_width // 2 - 2, 0, 4, screen_height, rl.LIGHTGRAY) # Separator line
        rl.end_drawing()

    rl.unload_render_texture(screen_player1)
    rl.unload_render_texture(screen_player2)
    rl.close_window()

if __name__ == '__main__':
    main()
