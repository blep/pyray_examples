"""raylib [text] example - Text Writing Animation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.4, last time updated with raylib 1.4
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2016-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - text writing anim")

    message = "This sample illustrates a text writing\nanimation effect! Check it out! ;)"

    frames_counter = 0

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        if rl.is_key_down(rl.KEY_SPACE):
            frames_counter += 8
        else:
            frames_counter += 1

        if rl.is_key_pressed(rl.KEY_ENTER):
            frames_counter = 0

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text(rl.text_subtext(message, 0, frames_counter//10), 210, 160, 20, rl.MAROON)

        rl.draw_text("PRESS [ENTER] to RESTART!", 240, 260, 20, rl.LIGHTGRAY)
        rl.draw_text("HOLD [SPACE] to SPEED UP!", 239, 300, 20, rl.LIGHTGRAY)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()