"""raylib [core] example - Basic window
Example complexity rating: [★☆☆☆] 1/4
Welcome to raylib!
To test examples, just press F6 and execute 'raylib_compile_execute' script
Note that compiled executable is placed in the same folder as .c file
To test the examples on Web, press F6 and execute 'raylib_compile_execute_web' script
Web version of the program is generated in the same folder as .c file
You can find all basic examples on C:\raylib\raylib\examples folder or
raylib official webpage: www.raylib.com
Enjoy using raylib. :)
Example originally created with raylib 1.0, last time updated with raylib 1.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - basic window")

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        # TODO: Update your variables here
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("Congrats! You created your first window!", 190, 200, 20, rl.LIGHTGRAY)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
