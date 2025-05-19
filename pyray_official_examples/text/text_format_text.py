"""raylib [text] example - Text formatting
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.1, last time updated with raylib 3.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - text formatting")

    score = 100020
    hiscore = 200450
    lives = 5

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        # TODO: Update your variables here

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text(f"Score: {score:08d}", 200, 80, 20, rl.RED)

        rl.draw_text(f"HiScore: {hiscore:08d}", 200, 120, 20, rl.GREEN)

        rl.draw_text(f"Lives: {lives:02d}", 200, 160, 40, rl.BLUE)

        rl.draw_text(f"Elapsed Time: {rl.get_frame_time()*1000:.2f} ms", 200, 220, 20, rl.BLACK)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()        # Close window and OpenGL context

if __name__ == "__main__":
    main()