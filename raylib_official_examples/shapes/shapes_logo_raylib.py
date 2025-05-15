"""raylib [shapes] example - Draw raylib logo using basic shapes
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.0, last time updated with raylib 1.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - raylib logo using shapes")

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # TODO: Update your variables here
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle(screen_width//2 - 128, screen_height//2 - 128, 256, 256, rl.BLACK)
        rl.draw_rectangle(screen_width//2 - 112, screen_height//2 - 112, 224, 224, rl.RAYWHITE)
        rl.draw_text("raylib", screen_width//2 - 44, screen_height//2 + 48, 50, rl.BLACK)

        rl.draw_text("this is NOT a texture!", 350, 370, 10, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()