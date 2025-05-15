"""raylib [shapes] example - rectangle scaling by mouse
Example complexity rating: [★★☆☆] 2/4
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

MOUSE_SCALE_MARK_SIZE = 12

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - rectangle scaling mouse")

    rec = rl.Rectangle(100, 100, 200, 80)

    mouse_position = rl.Vector2(0, 0)

    mouse_scale_ready = False
    mouse_scale_mode = False

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        mouse_position = rl.get_mouse_position()

        scale_rec = rl.Rectangle(
            rec.x + rec.width - MOUSE_SCALE_MARK_SIZE, 
            rec.y + rec.height - MOUSE_SCALE_MARK_SIZE, 
            MOUSE_SCALE_MARK_SIZE, 
            MOUSE_SCALE_MARK_SIZE
        )

        if rl.check_collision_point_rec(mouse_position, scale_rec):
            mouse_scale_ready = True
            if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
                mouse_scale_mode = True
        else:
            mouse_scale_ready = False

        if mouse_scale_mode:
            mouse_scale_ready = True

            rec.width = (mouse_position.x - rec.x)
            rec.height = (mouse_position.y - rec.y)

            # Check minimum rec size
            if rec.width < MOUSE_SCALE_MARK_SIZE:
                rec.width = MOUSE_SCALE_MARK_SIZE
            if rec.height < MOUSE_SCALE_MARK_SIZE:
                rec.height = MOUSE_SCALE_MARK_SIZE
            
            # Check maximum rec size
            if rec.width > (rl.get_screen_width() - rec.x):
                rec.width = rl.get_screen_width() - rec.x
            if rec.height > (rl.get_screen_height() - rec.y):
                rec.height = rl.get_screen_height() - rec.y

            if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
                mouse_scale_mode = False
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("Scale rectangle dragging from bottom-right corner!", 10, 10, 20, rl.GRAY)

        rl.draw_rectangle_rec(rec, rl.fade(rl.GREEN, 0.5))

        if mouse_scale_ready:
            rl.draw_rectangle_lines_ex(rec, 1, rl.RED)
            rl.draw_triangle(
                rl.Vector2(rec.x + rec.width - MOUSE_SCALE_MARK_SIZE, rec.y + rec.height),
                rl.Vector2(rec.x + rec.width, rec.y + rec.height),
                rl.Vector2(rec.x + rec.width, rec.y + rec.height - MOUSE_SCALE_MARK_SIZE), 
                rl.RED
            )

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()