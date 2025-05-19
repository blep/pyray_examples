"""raylib [shapes] example - easings ball anim
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
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

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - easings ball anim")

    # Ball variable value to be animated with easings
    ball_position_x = -100
    ball_radius = 20
    ball_alpha = 0.0

    state = 0
    frames_counter = 0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if state == 0:             # Move ball position X with easing
            frames_counter += 1
            ball_position_x = int(rl.ease_elastic_out(float(frames_counter), -100, screen_width/2.0 + 100, 120))

            if frames_counter >= 120:
                frames_counter = 0
                state = 1
        elif state == 1:        # Increase ball radius with easing
            frames_counter += 1
            ball_radius = int(rl.ease_elastic_in(float(frames_counter), 20, 500, 200))

            if frames_counter >= 200:
                frames_counter = 0
                state = 2
        elif state == 2:        # Change ball alpha with easing (background color blending)
            frames_counter += 1
            ball_alpha = rl.ease_cubic_out(float(frames_counter), 0.0, 1.0, 200)

            if frames_counter >= 200:
                frames_counter = 0
                state = 3
        elif state == 3:        # Reset state to play again
            if rl.is_key_pressed(rl.KEY_ENTER):
                # Reset required variables to play again
                ball_position_x = -100
                ball_radius = 20
                ball_alpha = 0.0
                state = 0

        if rl.is_key_pressed(rl.KEY_R):
            frames_counter = 0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        if state >= 2:
            rl.draw_rectangle(0, 0, screen_width, screen_height, rl.GREEN)
        
        rl.draw_circle(ball_position_x, 200, float(ball_radius), rl.fade(rl.RED, 1.0 - ball_alpha))

        if state == 3:
            rl.draw_text("PRESS [ENTER] TO PLAY AGAIN!", 240, 200, 20, rl.BLACK)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()