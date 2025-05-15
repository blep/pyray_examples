"""raylib [core] example - 2d camera split screen
Example complexity rating: [★★★★] 4/4
Addapted from the core_3d_camera_split_screen example: 
    https://github.com/raysan5/raylib/blob/master/examples/core/core_3d_camera_split_screen.c
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by Gabriel dos Santos Sanches (@gabrielssanches) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Gabriel dos Santos Sanches (@gabrielssanches)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

PLAYER_SIZE = 40

def main():
    screen_width = 800
    screen_height = 440

    rl.init_window(screen_width, screen_height, "raylib [core] example - 2d camera split screen")

    player1 = rl.Rectangle(200, 200, PLAYER_SIZE, PLAYER_SIZE)
    player2 = rl.Rectangle(250, 200, PLAYER_SIZE, PLAYER_SIZE)

    camera1 = rl.Camera2D()
    camera1.target = rl.Vector2(player1.x, player1.y)
    camera1.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0) # Adjusted for typical 2D camera setup
    camera1.rotation = 0.0
    camera1.zoom = 1.0

    camera2 = rl.Camera2D()
    camera2.target = rl.Vector2(player2.x, player2.y)
    camera2.offset = rl.Vector2(screen_width / 2.0, screen_height / 2.0) # Adjusted for typical 2D camera setup
    camera2.rotation = 0.0
    camera2.zoom = 1.0

    # Render textures for each camera view
    # Halve the width for split screen, full height
    screen_camera1 = rl.load_render_texture(screen_width // 2, screen_height)
    screen_camera2 = rl.load_render_texture(screen_width // 2, screen_height)

    # Rectangle for drawing the render texture, flipped vertically due to OpenGL coordinates
    split_screen_rect = rl.Rectangle(0, 0, float(screen_camera1.texture.width), float(-screen_camera1.texture.height))

    rl.set_target_fps(60)

    while not rl.window_should_close():
        # Update
        if rl.is_key_down(rl.KEY_S):
            player1.y += 3.0
        elif rl.is_key_down(rl.KEY_W):
            player1.y -= 3.0
        if rl.is_key_down(rl.KEY_D):
            player1.x += 3.0
        elif rl.is_key_down(rl.KEY_A):
            player1.x -= 3.0

        if rl.is_key_down(rl.KEY_UP):
            player2.y -= 3.0
        elif rl.is_key_down(rl.KEY_DOWN):
            player2.y += 3.0
        if rl.is_key_down(rl.KEY_RIGHT):
            player2.x += 3.0
        elif rl.is_key_down(rl.KEY_LEFT):
            player2.x -= 3.0

        camera1.target = rl.Vector2(player1.x + player1.width / 2, player1.y + player1.height / 2) # Target center of player
        camera2.target = rl.Vector2(player2.x + player2.width / 2, player2.y + player2.height / 2) # Target center of player

        # Draw to render texture for camera 1
        rl.begin_texture_mode(screen_camera1)
        rl.clear_background(rl.RAYWHITE)
        rl.begin_mode_2d(camera1)

        # Draw scene for camera 1
        for i in range(screen_width // PLAYER_SIZE + 1):
            rl.draw_line_v(rl.Vector2(float(PLAYER_SIZE * i), 0), rl.Vector2(float(PLAYER_SIZE * i), float(screen_height)), rl.LIGHTGRAY)
        for i in range(screen_height // PLAYER_SIZE + 1):
            rl.draw_line_v(rl.Vector2(0, float(PLAYER_SIZE * i)), rl.Vector2(float(screen_width), float(PLAYER_SIZE * i)), rl.LIGHTGRAY)
        for i in range(screen_width // PLAYER_SIZE):
            for j in range(screen_height // PLAYER_SIZE):
                rl.draw_text(f"[{i},{j}]", 10 + PLAYER_SIZE * i, 15 + PLAYER_SIZE * j, 10, rl.LIGHTGRAY)
        
        rl.draw_rectangle_rec(player1, rl.RED)
        rl.draw_rectangle_rec(player2, rl.BLUE)

        rl.end_mode_2d()
        rl.draw_rectangle(0, 0, screen_width // 2, 30, rl.fade(rl.RAYWHITE, 0.6))
        rl.draw_text("PLAYER1: W/S/A/D to move", 10, 10, 10, rl.MAROON)
        rl.end_texture_mode()

        # Draw to render texture for camera 2
        rl.begin_texture_mode(screen_camera2)
        rl.clear_background(rl.RAYWHITE)
        rl.begin_mode_2d(camera2)

        # Draw scene for camera 2 (same scene, different camera)
        for i in range(screen_width // PLAYER_SIZE + 1):
            rl.draw_line_v(rl.Vector2(float(PLAYER_SIZE * i), 0), rl.Vector2(float(PLAYER_SIZE * i), float(screen_height)), rl.LIGHTGRAY)
        for i in range(screen_height // PLAYER_SIZE + 1):
            rl.draw_line_v(rl.Vector2(0, float(PLAYER_SIZE * i)), rl.Vector2(float(screen_width), float(PLAYER_SIZE * i)), rl.LIGHTGRAY)
        for i in range(screen_width // PLAYER_SIZE):
            for j in range(screen_height // PLAYER_SIZE):
                rl.draw_text(f"[{i},{j}]", 10 + PLAYER_SIZE * i, 15 + PLAYER_SIZE * j, 10, rl.LIGHTGRAY)

        rl.draw_rectangle_rec(player1, rl.RED)
        rl.draw_rectangle_rec(player2, rl.BLUE)

        rl.end_mode_2d()
        rl.draw_rectangle(0, 0, screen_width // 2, 30, rl.fade(rl.RAYWHITE, 0.6))
        rl.draw_text("PLAYER2: UP/DOWN/LEFT/RIGHT to move", 10, 10, 10, rl.DARKBLUE)
        rl.end_texture_mode()

        # Draw both render textures to the screen
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        rl.draw_texture_rec(screen_camera1.texture, split_screen_rect, rl.Vector2(0, 0), rl.WHITE)
        rl.draw_texture_rec(screen_camera2.texture, split_screen_rect, rl.Vector2(screen_width / 2.0, 0), rl.WHITE)
        # Draw a line separating the two views
        rl.draw_rectangle(screen_width // 2 - 2, 0, 4, screen_height, rl.LIGHTGRAY)
        rl.end_drawing()

    rl.unload_render_texture(screen_camera1)
    rl.unload_render_texture(screen_camera2)
    rl.close_window()

if __name__ == '__main__':
    main()
