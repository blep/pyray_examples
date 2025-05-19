"""raylib [shapes] example - raylib logo animation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 4.0
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

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - raylib logo animation")

    logo_position_x = screen_width//2 - 128
    logo_position_y = screen_height//2 - 128

    frames_counter = 0
    letters_count = 0

    top_side_rec_width = 16
    left_side_rec_height = 16

    bottom_side_rec_width = 16
    right_side_rec_height = 16

    state = 0                  # Tracking animation states (State Machine)
    alpha = 1.0                # Useful for fading

    rl.set_target_fps(60)      # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if state == 0:                 # State 0: Small box blinking
            frames_counter += 1

            if frames_counter == 120:
                state = 1
                frames_counter = 0      # Reset counter... will be used later...
        
        elif state == 1:            # State 1: Top and left bars growing
            top_side_rec_width += 4
            left_side_rec_height += 4

            if top_side_rec_width == 256:
                state = 2
        
        elif state == 2:            # State 2: Bottom and right bars growing
            bottom_side_rec_width += 4
            right_side_rec_height += 4

            if bottom_side_rec_width == 256:
                state = 3
        
        elif state == 3:            # State 3: Letters appearing (one by one)
            frames_counter += 1

            if frames_counter//12:       # Every 12 frames, one more letter!
                letters_count += 1
                frames_counter = 0

            if letters_count >= 10:     # When all letters have appeared, just fade out everything
                alpha -= 0.02

                if alpha <= 0.0:
                    alpha = 0.0
                    state = 4
        
        elif state == 4:            # State 4: Reset and Replay
            if rl.is_key_pressed(rl.KEY_R):
                frames_counter = 0
                letters_count = 0

                top_side_rec_width = 16
                left_side_rec_height = 16

                bottom_side_rec_width = 16
                right_side_rec_height = 16

                alpha = 1.0
                state = 0          # Return to State 0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        if state == 0:
            if (frames_counter//15)%2:
                rl.draw_rectangle(logo_position_x, logo_position_y, 16, 16, rl.BLACK)
        
        elif state == 1:
            rl.draw_rectangle(logo_position_x, logo_position_y, top_side_rec_width, 16, rl.BLACK)
            rl.draw_rectangle(logo_position_x, logo_position_y, 16, left_side_rec_height, rl.BLACK)
        
        elif state == 2:
            rl.draw_rectangle(logo_position_x, logo_position_y, top_side_rec_width, 16, rl.BLACK)
            rl.draw_rectangle(logo_position_x, logo_position_y, 16, left_side_rec_height, rl.BLACK)

            rl.draw_rectangle(logo_position_x + 240, logo_position_y, 16, right_side_rec_height, rl.BLACK)
            rl.draw_rectangle(logo_position_x, logo_position_y + 240, bottom_side_rec_width, 16, rl.BLACK)
        
        elif state == 3:
            rl.draw_rectangle(logo_position_x, logo_position_y, top_side_rec_width, 16, rl.fade(rl.BLACK, alpha))
            rl.draw_rectangle(logo_position_x, logo_position_y + 16, 16, left_side_rec_height - 32, rl.fade(rl.BLACK, alpha))

            rl.draw_rectangle(logo_position_x + 240, logo_position_y + 16, 16, right_side_rec_height - 32, rl.fade(rl.BLACK, alpha))
            rl.draw_rectangle(logo_position_x, logo_position_y + 240, bottom_side_rec_width, 16, rl.fade(rl.BLACK, alpha))

            rl.draw_rectangle(rl.get_screen_width()//2 - 112, rl.get_screen_height()//2 - 112, 224, 224, rl.fade(rl.RAYWHITE, alpha))

            rl.draw_text(rl.text_subtext("raylib", 0, letters_count), rl.get_screen_width()//2 - 44, rl.get_screen_height()//2 + 48, 50, rl.fade(rl.BLACK, alpha))
        
        elif state == 4:
            rl.draw_text("[R] REPLAY", 340, 200, 20, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()