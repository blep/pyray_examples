"""raylib [core] example - Storage save/load values
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.4, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random

# Storage positions
STORAGE_POSITION_SCORE = 0
STORAGE_POSITION_HISCORE = 1

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - storage save/load values")

    score = 0
    hiscore = 0
    frames_counter = 0

    rl.set_target_fps(60)

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KEY_R):
            score = random.randint(1000, 2000)
            hiscore = random.randint(2000, 4000)

        if rl.is_key_pressed(rl.KEY_ENTER):
            rl.save_storage_value(STORAGE_POSITION_SCORE, score)
            rl.save_storage_value(STORAGE_POSITION_HISCORE, hiscore)
        elif rl.is_key_pressed(rl.KEY_SPACE):
            score = rl.load_storage_value(STORAGE_POSITION_SCORE)
            hiscore = rl.load_storage_value(STORAGE_POSITION_HISCORE)

        frames_counter += 1

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.draw_text(f"SCORE: {score}", 280, 130, 40, rl.MAROON)
        rl.draw_text(f"HI-SCORE: {hiscore}", 210, 200, 50, rl.BLACK)

        rl.draw_text(f"frames: {frames_counter}", 10, 10, 20, rl.LIME)

        rl.draw_text("Press R to generate random numbers", 220, 40, 20, rl.LIGHTGRAY)
        rl.draw_text("Press ENTER to SAVE values", 250, 310, 20, rl.LIGHTGRAY)
        rl.draw_text("Press SPACE to LOAD values", 252, 350, 20, rl.LIGHTGRAY)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
