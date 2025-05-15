"""raylib [shapes] example - draw circle sector (with gui options)
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example contributed by Vlad Adrian (@demizdor) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Vlad Adrian (@demizdor) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import math
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - draw circle sector")

    center = rl.Vector2((rl.get_screen_width() - 300)/2.0, rl.get_screen_height()/2.0)

    outer_radius = rl.ffi.new('float *', 180.0)
    start_angle = rl.ffi.new('float *', 0.0)
    end_angle = rl.ffi.new('float *', 180.0)
    segments = rl.ffi.new('float *', 10.0)
    min_segments = 4.0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # NOTE: All variables update happens inside GUI control functions
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_line(500, 0, 500, rl.get_screen_height(), rl.fade(rl.LIGHTGRAY, 0.6))
        rl.draw_rectangle(500, 0, rl.get_screen_width() - 500, rl.get_screen_height(), rl.fade(rl.LIGHTGRAY, 0.3))

        rl.draw_circle_sector(center, outer_radius[0], start_angle[0], end_angle[0], int(segments[0]), rl.fade(rl.MAROON, 0.3))
        rl.draw_circle_sector_lines(center, outer_radius[0], start_angle[0], end_angle[0], int(segments[0]), rl.fade(rl.MAROON, 0.6))

        # Draw GUI controls
        #------------------------------------------------------------------------------
        rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle[0]:.2f}", start_angle, 0, 720)
        rl.gui_slider_bar(rl.Rectangle(600, 70, 120, 20), "EndAngle", f"{end_angle[0]:.2f}", end_angle, 0, 720)

        rl.gui_slider_bar(rl.Rectangle(600, 140, 120, 20), "Radius", f"{outer_radius[0]:.2f}", outer_radius, 0, 200)
        rl.gui_slider_bar(rl.Rectangle(600, 170, 120, 20), "Segments", f"{segments[0]:.2f}", segments, 0, 100)
        #------------------------------------------------------------------------------

        min_segments = math.trunc(math.ceil((end_angle[0] - start_angle[0]) / 90))
        mode_text = f"MODE: {'MANUAL' if segments[0] >= min_segments else 'AUTO'}"
        rl.draw_text(mode_text, 600, 200, 10, rl.MAROON if segments[0] >= min_segments else rl.DARKGRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()