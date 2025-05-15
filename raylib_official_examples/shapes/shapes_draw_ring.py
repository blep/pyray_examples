"""raylib [shapes] example - draw ring (with gui options)
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

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - draw ring")

    center = rl.Vector2((rl.get_screen_width() - 300)/2.0, rl.get_screen_height()/2.0)

    inner_radius = 80.0
    outer_radius = 190.0

    start_angle = 0.0
    end_angle = 360.0
    segments = 0.0

    draw_ring = True
    draw_ring_lines = False
    draw_circle_lines = False

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

        if draw_ring: 
            rl.draw_ring(center, inner_radius, outer_radius, start_angle, end_angle, int(segments), rl.fade(rl.MAROON, 0.3))
        if draw_ring_lines: 
            rl.draw_ring_lines(center, inner_radius, outer_radius, start_angle, end_angle, int(segments), rl.fade(rl.BLACK, 0.4))
        if draw_circle_lines: 
            rl.draw_circle_sector_lines(center, outer_radius, start_angle, end_angle, int(segments), rl.fade(rl.BLACK, 0.4))
            
        # Draw GUI controls
        #------------------------------------------------------------------------------
        start_angle_ptr = rl.ffi.new('float *', start_angle)
        rl.gui_slider_bar(rl.Rectangle(600, 40, 120, 20), "StartAngle", f"{start_angle_ptr[0]:.2f}", start_angle_ptr, -450, 450)
        start_angle = start_angle_ptr[0]
        
        end_angle_ptr = rl.ffi.new('float *', end_angle)
        rl.gui_slider_bar(rl.Rectangle(600, 70, 120, 20), "EndAngle", f"{end_angle_ptr[0]:.2f}", end_angle_ptr, -450, 450)
        end_angle = end_angle_ptr[0]

        inner_radius_ptr = rl.ffi.new('float *', inner_radius)
        rl.gui_slider_bar(rl.Rectangle(600, 140, 120, 20), "InnerRadius", f"{inner_radius_ptr[0]:.2f}", inner_radius_ptr, 0, 100)
        inner_radius = inner_radius_ptr[0]
        
        outer_radius_ptr = rl.ffi.new('float *', outer_radius)
        rl.gui_slider_bar(rl.Rectangle(600, 170, 120, 20), "OuterRadius", f"{outer_radius_ptr[0]:.2f}", outer_radius_ptr, 0, 200)
        outer_radius = outer_radius_ptr[0]

        segments_ptr = rl.ffi.new('float *', segments)
        rl.gui_slider_bar(rl.Rectangle(600, 240, 120, 20), "Segments", f"{segments_ptr[0]:.2f}", segments_ptr, 0, 100)
        segments = segments_ptr[0]
        
        draw_ring_ptr = rl.ffi.new('bool *', draw_ring)
        rl.gui_check_box(rl.Rectangle(600, 320, 20, 20), "Draw Ring", draw_ring_ptr)
        draw_ring = draw_ring_ptr[0]
        
        draw_ring_lines_ptr = rl.ffi.new('bool *', draw_ring_lines)
        rl.gui_check_box(rl.Rectangle(600, 350, 20, 20), "Draw RingLines", draw_ring_lines_ptr)
        draw_ring_lines = draw_ring_lines_ptr[0]
        
        draw_circle_lines_ptr = rl.ffi.new('bool *', draw_circle_lines)
        rl.gui_check_box(rl.Rectangle(600, 380, 20, 20), "Draw CircleLines", draw_circle_lines_ptr)
        draw_circle_lines = draw_circle_lines_ptr[0]
        #------------------------------------------------------------------------------

        min_segments = math.ceil((end_angle - start_angle)/90)
        mode_text = f"MODE: {'MANUAL' if segments >= min_segments else 'AUTO'}"
        rl.draw_text(mode_text, 600, 270, 10, rl.MAROON if segments >= min_segments else rl.DARKGRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()