"""raylib [core] example - Basic window (adapted for HTML5 platform)
Example complexity rating: [★☆☆☆] 1/4
NOTE: This example is prepared to compile for PLATFORM_WEB, and PLATFORM_DESKTOP
As you will notice, code structure is slightly diferent to the other examples...
To compile it for PLATFORM_WEB just uncomment #define PLATFORM_WEB at beginning
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

# Global Variables Definition (equivalent to C example)
# In Python, these would typically be defined within main or a class if not truly global.
# For direct translation, we'll define them here, though it's less common in Python for simple scripts.
screen_width = 800
screen_height = 450

# Module functions declaration (equivalent to C example)
def update_draw_frame():
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

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    rl.init_window(screen_width, screen_height, "raylib [core] example - basic window (web-adapted structure)")

    # pyray handles the web loop differently if you compile with emscripten.
    # For a standard desktop Python script, we use SetTargetFPS and a while loop.
    # If this script were to be compiled for web using something like raylibpycpp's web support,
    # the underlying raylib C calls would handle the emscripten_set_main_loop.
    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        update_draw_frame()

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
