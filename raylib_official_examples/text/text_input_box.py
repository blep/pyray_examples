"""raylib [text] example - Input Box
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.7, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

MAX_INPUT_CHARS = 9

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - input box")

    name = ""  # In Python, strings are mutable, so we don't need a fixed size buffer
    letter_count = 0

    text_box = rl.Rectangle(screen_width/2.0 - 100, 180, 225, 50)
    mouse_on_text = False

    frames_counter = 0

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        if rl.check_collision_point_rec(rl.get_mouse_position(), text_box):
            mouse_on_text = True
        else:
            mouse_on_text = False

        if mouse_on_text:
            # Set the window's cursor to the I-Beam
            rl.set_mouse_cursor(rl.MOUSE_CURSOR_IBEAM)

            # Get char pressed (unicode character) on the queue
            key = rl.get_char_pressed()

            # Check if more characters have been pressed on the same frame
            while key > 0:
                # NOTE: Only allow keys in range [32..125]
                if (key >= 32) and (key <= 125) and (letter_count < MAX_INPUT_CHARS):
                    name += chr(key)
                    letter_count += 1

                key = rl.get_char_pressed()  # Check next character in the queue

            if rl.is_key_pressed(rl.KEY_BACKSPACE):
                name = name[:-1]  # Remove last character
                letter_count -= 1
                if letter_count < 0:
                    letter_count = 0
        else:
            rl.set_mouse_cursor(rl.MOUSE_CURSOR_DEFAULT)

        if mouse_on_text:
            frames_counter += 1
        else:
            frames_counter = 0

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("PLACE MOUSE OVER INPUT BOX!", 240, 140, 20, rl.GRAY)

        rl.draw_rectangle_rec(text_box, rl.LIGHTGRAY)
        if mouse_on_text:
            rl.draw_rectangle_lines(int(text_box.x), int(text_box.y), int(text_box.width), int(text_box.height), rl.RED)
        else:
            rl.draw_rectangle_lines(int(text_box.x), int(text_box.y), int(text_box.width), int(text_box.height), rl.DARKGRAY)

        rl.draw_text(name, int(text_box.x) + 5, int(text_box.y) + 8, 40, rl.MAROON)

        rl.draw_text(f"INPUT CHARS: {letter_count}/{MAX_INPUT_CHARS}", 315, 250, 20, rl.DARKGRAY)

        if mouse_on_text:
            if letter_count < MAX_INPUT_CHARS:
                # Draw blinking underscore char
                if ((frames_counter//20) % 2) == 0:
                    rl.draw_text("_", int(text_box.x) + 8 + rl.measure_text(name, 40), int(text_box.y) + 12, 40, rl.MAROON)
            else:
                rl.draw_text("Press BACKSPACE to delete chars...", 230, 300, 20, rl.GRAY)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()  # Close window and OpenGL context

# Helper function - Check if any key is pressed
# NOTE: We limit keys check to keys between 32 (KEY_SPACE) and 126
def is_any_key_pressed():
    key_pressed = False
    key = rl.get_key_pressed()

    if (key >= 32) and (key <= 126):
        key_pressed = True

    return key_pressed

if __name__ == "__main__":
    main()