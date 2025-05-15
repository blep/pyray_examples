"""raylib [shapes] example - draw rectangle rounded (with gui options)
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
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - draw rectangle rounded")

    roundness = 0.2
    width = 200.0
    height = 100.0
    segments = 0.0
    line_thick = 1.0

    draw_rect = False
    draw_rounded_rect = True
    draw_rounded_lines = False

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rec = rl.Rectangle((rl.get_screen_width() - width - 250)/2, 
                          (rl.get_screen_height() - height)/2.0,
                          width, height)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_line(560, 0, 560, rl.get_screen_height(), rl.fade(rl.LIGHTGRAY, 0.6))
        rl.draw_rectangle(560, 0, rl.get_screen_width() - 500, rl.get_screen_height(), rl.fade(rl.LIGHTGRAY, 0.3))

        if draw_rect:
            rl.draw_rectangle_rec(rec, rl.fade(rl.GOLD, 0.6))
        if draw_rounded_rect:
            rl.draw_rectangle_rounded(rec, roundness, int(segments), rl.fade(rl.MAROON, 0.2))
        if draw_rounded_lines:
            rl.draw_rectangle_rounded_lines_ex(rec, roundness, int(segments), line_thick, rl.fade(rl.MAROON, 0.4))        # Draw GUI controls
        #------------------------------------------------------------------------------
        width_ptr = rl.ffi.new('float *', width)
        rl.gui_slider_bar(rl.Rectangle(640, 40, 105, 20), "Width", f"{width_ptr[0]:.2f}", width_ptr, 0, float(rl.get_screen_width() - 300))
        width = width_ptr[0]
        
        height_ptr = rl.ffi.new('float *', height)
        rl.gui_slider_bar(rl.Rectangle(640, 70, 105, 20), "Height", f"{height_ptr[0]:.2f}", height_ptr, 0, float(rl.get_screen_height() - 50))
        height = height_ptr[0]
        
        roundness_ptr = rl.ffi.new('float *', roundness)
        rl.gui_slider_bar(rl.Rectangle(640, 140, 105, 20), "Roundness", f"{roundness_ptr[0]:.2f}", roundness_ptr, 0.0, 1.0)
        roundness = roundness_ptr[0]
        
        line_thick_ptr = rl.ffi.new('float *', line_thick)
        rl.gui_slider_bar(rl.Rectangle(640, 170, 105, 20), "Thickness", f"{line_thick_ptr[0]:.2f}", line_thick_ptr, 0, 20)
        line_thick = line_thick_ptr[0]
        segments_ptr = rl.ffi.new('float *', segments)
        rl.gui_slider_bar(rl.Rectangle(640, 240, 105, 20), "Segments", f"{segments_ptr[0]:.2f}", segments_ptr, 0, 60)
        segments = segments_ptr[0]
        
        draw_rounded_rect_ptr = rl.ffi.new('bool *', draw_rounded_rect)
        rl.gui_check_box(rl.Rectangle(640, 320, 20, 20), "DrawRoundedRect", draw_rounded_rect_ptr)
        draw_rounded_rect = draw_rounded_rect_ptr[0]
        
        draw_rounded_lines_ptr = rl.ffi.new('bool *', draw_rounded_lines)
        rl.gui_check_box(rl.Rectangle(640, 350, 20, 20), "DrawRoundedLines", draw_rounded_lines_ptr)
        draw_rounded_lines = draw_rounded_lines_ptr[0]
        
        draw_rect_ptr = rl.ffi.new('bool *', draw_rect)
        rl.gui_check_box(rl.Rectangle(640, 380, 20, 20), "DrawRect", draw_rect_ptr)
        draw_rect = draw_rect_ptr[0]
        #------------------------------------------------------------------------------

        mode_text = f"MODE: {'MANUAL' if segments >= 4 else 'AUTO'}"
        rl.draw_text(mode_text, 640, 280, 10, rl.MAROON if segments >= 4 else rl.DARKGRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()