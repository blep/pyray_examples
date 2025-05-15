"""raylib [shapes] example - Colors palette
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.0, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

MAX_COLORS_COUNT = 21          # Number of colors available

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - colors palette")

    colors = [
        rl.DARKGRAY, rl.MAROON, rl.ORANGE, rl.DARKGREEN, rl.DARKBLUE, rl.DARKPURPLE, rl.DARKBROWN,
        rl.GRAY, rl.RED, rl.GOLD, rl.LIME, rl.BLUE, rl.VIOLET, rl.BROWN, rl.LIGHTGRAY, rl.PINK, rl.YELLOW,
        rl.GREEN, rl.SKYBLUE, rl.PURPLE, rl.BEIGE
    ]

    color_names = [
        "DARKGRAY", "MAROON", "ORANGE", "DARKGREEN", "DARKBLUE", "DARKPURPLE",
        "DARKBROWN", "GRAY", "RED", "GOLD", "LIME", "BLUE", "VIOLET", "BROWN",
        "LIGHTGRAY", "PINK", "YELLOW", "GREEN", "SKYBLUE", "PURPLE", "BEIGE"
    ]

    colors_recs = [rl.Rectangle(0, 0, 0, 0) for _ in range(MAX_COLORS_COUNT)]     # Rectangles array

    # Fills colorsRecs data (for every rectangle)
    for i in range(MAX_COLORS_COUNT):
        colors_recs[i].x = 20.0 + 100.0 * (i % 7) + 10.0 * (i % 7)
        colors_recs[i].y = 80.0 + 100.0 * (i // 7) + 10.0 * (i // 7)
        colors_recs[i].width = 100.0
        colors_recs[i].height = 100.0

    color_state = [0] * MAX_COLORS_COUNT           # Color state: 0-DEFAULT, 1-MOUSE_HOVER

    mouse_point = rl.Vector2(0.0, 0.0)

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        mouse_point = rl.get_mouse_position()

        for i in range(MAX_COLORS_COUNT):
            if rl.check_collision_point_rec(mouse_point, colors_recs[i]):
                color_state[i] = 1
            else:
                color_state[i] = 0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("raylib colors palette", 28, 42, 20, rl.BLACK)
        rl.draw_text("press SPACE to see all colors", rl.get_screen_width() - 180, rl.get_screen_height() - 40, 10, rl.GRAY)

        for i in range(MAX_COLORS_COUNT):    # Draw all rectangles
            rl.draw_rectangle_rec(colors_recs[i], rl.fade(colors[i], 0.6 if color_state[i] else 1.0))

            if rl.is_key_down(rl.KEY_SPACE) or color_state[i]:
                rl.draw_rectangle(int(colors_recs[i].x), int(colors_recs[i].y + colors_recs[i].height - 26), 
                                 int(colors_recs[i].width), 20, rl.BLACK)
                rl.draw_rectangle_lines_ex(colors_recs[i], 6, rl.fade(rl.BLACK, 0.3))
                rl.draw_text(color_names[i], int(colors_recs[i].x + colors_recs[i].width - rl.measure_text(color_names[i], 10) - 12),
                           int(colors_recs[i].y + colors_recs[i].height - 20), 10, colors[i])

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()                # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()