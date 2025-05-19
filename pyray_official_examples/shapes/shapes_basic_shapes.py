"""raylib [shapes] example - Draw basic shapes 2d (rectangle, circle, line...)
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.0, last time updated with raylib 4.2
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

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - basic shapes drawing")

    rotation = 0.0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rotation += 0.2
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("some basic shapes available on raylib", 20, 20, 20, rl.DARKGRAY)

        # Circle shapes and lines
        rl.draw_circle(screen_width//5, 120, 35, rl.DARKBLUE)
        rl.draw_circle_gradient(screen_width//5, 220, 60, rl.GREEN, rl.SKYBLUE)
        rl.draw_circle_lines(screen_width//5, 340, 80, rl.DARKBLUE)

        # Rectangle shapes and lines
        rl.draw_rectangle(screen_width//4*2 - 60, 100, 120, 60, rl.RED)
        rl.draw_rectangle_gradient_h(screen_width//4*2 - 90, 170, 180, 130, rl.MAROON, rl.GOLD)
        rl.draw_rectangle_lines(screen_width//4*2 - 40, 320, 80, 60, rl.ORANGE)  # NOTE: Uses QUADS internally, not lines

        # Triangle shapes and lines
        rl.draw_triangle(
            rl.Vector2(screen_width/4.0 *3.0, 80.0),
            rl.Vector2(screen_width/4.0 *3.0 - 60.0, 150.0),
            rl.Vector2(screen_width/4.0 *3.0 + 60.0, 150.0), 
            rl.VIOLET
        )

        rl.draw_triangle_lines(
            rl.Vector2(screen_width/4.0*3.0, 160.0),
            rl.Vector2(screen_width/4.0*3.0 - 20.0, 230.0),
            rl.Vector2(screen_width/4.0*3.0 + 20.0, 230.0), 
            rl.DARKBLUE
        )

        # Polygon shapes and lines
        rl.draw_poly(rl.Vector2(screen_width/4.0*3, 330), 6, 80, rotation, rl.BROWN)
        rl.draw_poly_lines(rl.Vector2(screen_width/4.0*3, 330), 6, 90, rotation, rl.BROWN)
        rl.draw_poly_lines_ex(rl.Vector2(screen_width/4.0*3, 330), 6, 85, rotation, 6, rl.BEIGE)

        # NOTE: We draw all LINES based shapes together to optimize internal drawing,
        # this way, all LINES are rendered in a single draw pass
        rl.draw_line(18, 42, screen_width - 18, 42, rl.BLACK)
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()