"""raylib [shapes] example - Cubic-bezier lines
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.7, last time updated with raylib 1.7
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

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

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "raylib [shapes] example - cubic-bezier lines")

    start_point = rl.Vector2(30, 30)
    end_point = rl.Vector2(screen_width - 30, screen_height - 30)
    move_start_point = False
    move_end_point = False

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        mouse = rl.get_mouse_position()

        if rl.check_collision_point_circle(mouse, start_point, 10.0) and rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            move_start_point = True
        elif rl.check_collision_point_circle(mouse, end_point, 10.0) and rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            move_end_point = True

        if move_start_point:
            start_point = mouse
            if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
                move_start_point = False

        if move_end_point:
            end_point = mouse
            if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
                move_end_point = False
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("MOVE START-END POINTS WITH MOUSE", 15, 20, 20, rl.GRAY)

        # Draw line Cubic Bezier, in-out interpolation (easing), no control points
        rl.draw_line_bezier(start_point, end_point, 4.0, rl.BLUE)
        
        # Draw start-end spline circles with some details
        start_radius = 14.0 if rl.check_collision_point_circle(mouse, start_point, 10.0) else 8.0
        end_radius = 14.0 if rl.check_collision_point_circle(mouse, end_point, 10.0) else 8.0
        
        rl.draw_circle_v(start_point, start_radius, rl.RED if move_start_point else rl.BLUE)
        rl.draw_circle_v(end_point, end_radius, rl.RED if move_end_point else rl.BLUE)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()