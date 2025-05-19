"""raylib [core] example - Keyboard input
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.0, last time updated with raylib 1.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - keyboard input")

    ball_position = rl.Vector2(float(screen_width) / 2, float(screen_height) / 2)

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
            ball_position.x += 2.0
        if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
            ball_position.x -= 2.0
        if rl.is_key_down(rl.KeyboardKey.KEY_UP):
            ball_position.y -= 2.0
        if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
            ball_position.y += 2.0
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("move the ball with arrow keys", 10, 10, 20, rl.DARKGRAY)

        rl.draw_circle_v(ball_position, 50, rl.MAROON)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
