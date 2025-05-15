"""raylib [shapes] example - easings box anim
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

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - easings box anim")

    # Box variables to be animated with easings
    rec = rl.Rectangle(rl.get_screen_width()/2.0, -100, 100, 100)
    rotation = 0.0
    alpha = 1.0

    state = 0
    frames_counter = 0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if state == 0:     # Move box down to center of screen
            frames_counter += 1

            # NOTE: Remember that 3rd parameter of easing function refers to
            # desired value variation, do not confuse it with expected final value!
            rec.y = rl.ease_elastic_out(float(frames_counter), -100, rl.get_screen_height()/2.0 + 100, 120)

            if frames_counter >= 120:
                frames_counter = 0
                state = 1
        
        elif state == 1:     # Scale box to an horizontal bar
            frames_counter += 1
            rec.height = rl.ease_bounce_out(float(frames_counter), 100, -90, 120)
            rec.width = rl.ease_bounce_out(float(frames_counter), 100, float(rl.get_screen_width()), 120)

            if frames_counter >= 120:
                frames_counter = 0
                state = 2
        
        elif state == 2:     # Rotate horizontal bar rectangle
            frames_counter += 1
            rotation = rl.ease_quad_out(float(frames_counter), 0.0, 270.0, 240)

            if frames_counter >= 240:
                frames_counter = 0
                state = 3
        
        elif state == 3:     # Increase bar size to fill all screen
            frames_counter += 1
            rec.height = rl.ease_circ_out(float(frames_counter), 10, float(rl.get_screen_width()), 120)

            if frames_counter >= 120:
                frames_counter = 0
                state = 4
        
        elif state == 4:     # Fade out animation
            frames_counter += 1
            alpha = rl.ease_sine_out(float(frames_counter), 1.0, -1.0, 160)

            if frames_counter >= 160:
                frames_counter = 0
                state = 5

        # Reset animation at any moment
        if rl.is_key_pressed(rl.KEY_SPACE):
            rec = rl.Rectangle(rl.get_screen_width()/2.0, -100, 100, 100)
            rotation = 0.0
            alpha = 1.0
            state = 0
            frames_counter = 0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle_pro(rec, rl.Vector2(rec.width/2, rec.height/2), rotation, rl.fade(rl.BLACK, alpha))

        rl.draw_text("PRESS [SPACE] TO RESET BOX ANIMATION!", 10, rl.get_screen_height() - 25, 20, rl.LIGHTGRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()