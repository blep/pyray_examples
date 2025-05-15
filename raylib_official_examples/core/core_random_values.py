"""raylib [core] example - Generate random values
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.1, last time updated with raylib 1.1
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random # Required for GetRandomValue

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - generate random values")

    # rl.set_random_seed(0xaabbccff)  # Set a custom random seed if desired, by default: time.time()
    # In Python, random.seed() can be used. pyray.set_random_seed might not exist or work the same way.
    # For GetRandomValue, pyray typically wraps raylib's C functions which use their own internal seed.
    # If specific seed control identical to C is needed, one might need to manage seeding carefully.
    # For this example, default seeding is usually fine.

    rand_value = rl.get_random_value(-8, 5)  # Get a random integer number between -8 and 5 (both included)

    frames_counter = 0  # Variable used to count frames

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        frames_counter += 1

        # Every two seconds (120 frames) a new random value is generated
        if (frames_counter // 120) % 2 == 1:
            rand_value = rl.get_random_value(-8, 5)
            frames_counter = 0  # Reset counter after generating new value to make it exactly 2 seconds interval
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("Every 2 seconds a new random value is generated:", 130, 100, 20, rl.MAROON)

        rl.draw_text(f"{rand_value}", 360, 180, 80, rl.LIGHTGRAY)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
