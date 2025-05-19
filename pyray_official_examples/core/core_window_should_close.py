"""raylib [core] example - Window should close
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - window should close")

    rl.set_exit_key(rl.KEY_NULL)  # Disable KEY_ESCAPE to close window, X-button still works

    exit_window_requested = False
    exit_window = False

    rl.set_target_fps(60)

    while not exit_window:
        if rl.window_should_close() or rl.is_key_pressed(rl.KEY_ESCAPE):
            exit_window_requested = True

        if exit_window_requested:
            if rl.is_key_pressed(rl.KEY_Y):
                exit_window = True
            elif rl.is_key_pressed(rl.KEY_N):
                exit_window_requested = False

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        if exit_window_requested:
            rl.draw_rectangle(0, 100, screen_width, 200, rl.BLACK)
            rl.draw_text("Are you sure you want to exit program? [Y/N]", 40, 180, 30, rl.WHITE)
        else:
            rl.draw_text("Try to close the window to get confirmation message!", 120, 200, 20, rl.LIGHTGRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
