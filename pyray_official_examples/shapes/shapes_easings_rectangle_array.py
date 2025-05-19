"""raylib [shapes] example - easings rectangle array
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires 'easings.h' library, provided on raylib/src. Just copy
the library to same directory as example or make sure it's available on include path.
Example originally created with raylib 2.0, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

RECS_WIDTH = 50
RECS_HEIGHT = 50

MAX_RECS_X = 800 // RECS_WIDTH
MAX_RECS_Y = 450 // RECS_HEIGHT

PLAY_TIME_IN_FRAMES = 240                 # At 60 fps = 4 seconds

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - easings rectangle array")

    recs = [rl.Rectangle(0, 0, 0, 0) for _ in range(MAX_RECS_X * MAX_RECS_Y)]

    for y in range(MAX_RECS_Y):
        for x in range(MAX_RECS_X):
            recs[y*MAX_RECS_X + x].x = RECS_WIDTH/2.0 + RECS_WIDTH*x
            recs[y*MAX_RECS_X + x].y = RECS_HEIGHT/2.0 + RECS_HEIGHT*y
            recs[y*MAX_RECS_X + x].width = RECS_WIDTH
            recs[y*MAX_RECS_X + x].height = RECS_HEIGHT

    rotation = 0.0
    frames_counter = 0
    state = 0                  # Rectangles animation state: 0-Playing, 1-Finished

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if state == 0:
            frames_counter += 1

            for i in range(MAX_RECS_X * MAX_RECS_Y):
                recs[i].height = rl.ease_circ_out(float(frames_counter), RECS_HEIGHT, -RECS_HEIGHT, PLAY_TIME_IN_FRAMES)
                recs[i].width = rl.ease_circ_out(float(frames_counter), RECS_WIDTH, -RECS_WIDTH, PLAY_TIME_IN_FRAMES)

                if recs[i].height < 0:
                    recs[i].height = 0
                if recs[i].width < 0:
                    recs[i].width = 0

                if (recs[i].height == 0) and (recs[i].width == 0):
                    state = 1   # Finish playing

                rotation = rl.ease_linear_in(float(frames_counter), 0.0, 360.0, PLAY_TIME_IN_FRAMES)
        
        elif (state == 1) and rl.is_key_pressed(rl.KEY_SPACE):
            # When animation has finished, press space to restart
            frames_counter = 0

            for i in range(MAX_RECS_X * MAX_RECS_Y):
                recs[i].height = RECS_HEIGHT
                recs[i].width = RECS_WIDTH

            state = 0
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        if state == 0:
            for i in range(MAX_RECS_X * MAX_RECS_Y):
                rl.draw_rectangle_pro(
                    recs[i], 
                    rl.Vector2(recs[i].width/2, recs[i].height/2),
                    rotation,
                    rl.RED
                )
        elif state == 1:
            rl.draw_text("PRESS [SPACE] TO PLAY AGAIN!", 240, 200, 20, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()