"""raylib [core] examples - Mouse wheel input
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.1, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - input mouse wheel")

    box_position_y = screen_height // 2 - 40
    scroll_speed = 4  # Scrolling speed in pixels

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        box_position_y -= int(rl.get_mouse_wheel_move() * scroll_speed)
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle(screen_width // 2 - 40, box_position_y, 80, 80, rl.MAROON)

        rl.draw_text("Use mouse wheel to move the cube up and down!", 10, 10, 20, rl.GRAY)
        rl.draw_text(f"Box position Y: {box_position_y:03}", 10, 40, 20, rl.LIGHTGRAY)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
