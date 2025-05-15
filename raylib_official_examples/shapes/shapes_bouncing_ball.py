"""raylib [shapes] example - bouncing ball
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #---------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "raylib [shapes] example - bouncing ball")

    ball_position = rl.Vector2(rl.get_screen_width()/2.0, rl.get_screen_height()/2.0)
    ball_speed = rl.Vector2(5.0, 4.0)
    ball_radius = 20

    pause = False
    frames_counter = 0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #----------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #-----------------------------------------------------
        if rl.is_key_pressed(rl.KEY_SPACE):
            pause = not pause

        if not pause:
            ball_position.x += ball_speed.x
            ball_position.y += ball_speed.y

            # Check walls collision for bouncing
            if (ball_position.x >= (rl.get_screen_width() - ball_radius)) or (ball_position.x <= ball_radius):
                ball_speed.x *= -1.0
            if (ball_position.y >= (rl.get_screen_height() - ball_radius)) or (ball_position.y <= ball_radius):
                ball_speed.y *= -1.0
        else:
            frames_counter += 1
        #-----------------------------------------------------

        # Draw
        #-----------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_circle_v(ball_position, ball_radius, rl.MAROON)
        rl.draw_text("PRESS SPACE to PAUSE BALL MOVEMENT", 10, rl.get_screen_height() - 25, 20, rl.LIGHTGRAY)

        # On pause, we draw a blinking message
        if pause and ((frames_counter//30)%2):
            rl.draw_text("PAUSED", 350, 200, 30, rl.GRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #-----------------------------------------------------

    # De-Initialization
    #---------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #----------------------------------------------------------

if __name__ == "__main__":
    main()