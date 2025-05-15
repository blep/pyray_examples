"""raylib [core] example - Mouse input
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.0, last time updated with raylib 5.5
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

    rl.init_window(screen_width, screen_height, "raylib [core] example - mouse input")

    ball_position = rl.Vector2(-100.0, -100.0)
    ball_color = rl.DARKBLUE
    is_cursor_hidden = 0

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # ---------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        if rl.is_key_pressed(rl.KeyboardKey.KEY_H):
            if is_cursor_hidden == 0:
                rl.hide_cursor()
                is_cursor_hidden = 1
            else:
                rl.show_cursor()
                is_cursor_hidden = 0
        
        ball_position = rl.get_mouse_position()

        if rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_LEFT):
            ball_color = rl.MAROON
        elif rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_MIDDLE):
            ball_color = rl.LIME
        elif rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_RIGHT):
            ball_color = rl.DARKBLUE
        elif rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_SIDE):
            ball_color = rl.PURPLE
        elif rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_EXTRA):
            ball_color = rl.YELLOW
        elif rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_FORWARD):
            ball_color = rl.ORANGE
        elif rl.is_mouse_button_pressed(rl.MouseButton.MOUSE_BUTTON_BACK):
            ball_color = rl.BEIGE
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_circle_v(ball_position, 40, ball_color)

        rl.draw_text("move ball with mouse and click mouse button to change color", 10, 10, 20, rl.DARKGRAY)
        rl.draw_text("Press 'H' to toggle cursor visibility", 10, 30, 20, rl.DARKGRAY)

        if is_cursor_hidden == 1:
            rl.draw_text("CURSOR HIDDEN", 20, 60, 20, rl.RED)
        else:
            rl.draw_text("CURSOR VISIBLE", 20, 60, 20, rl.LIME)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
