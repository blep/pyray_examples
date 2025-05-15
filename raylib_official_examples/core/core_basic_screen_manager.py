"""raylib [core] examples - basic screen manager
Example complexity rating: [★☆☆☆] 1/4
NOTE: This example illustrates a very simple screen manager based on a states machines
Example originally created with raylib 4.0, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from enum import Enum # To define GameScreen enum

# GameScreen enum definition
class GameScreen(Enum):
    LOGO = 0
    TITLE = 1
    GAMEPLAY = 2
    ENDING = 3

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - basic screen manager")

    current_screen = GameScreen.LOGO
    frames_counter = 0  # Useful to count frames

    rl.set_target_fps(60)  # Set desired framerate (frames-per-second)

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        if current_screen == GameScreen.LOGO:
            frames_counter += 1
            # Wait for 2 seconds (120 frames) before jumping to TITLE screen
            if frames_counter > 120:
                current_screen = GameScreen.TITLE
                frames_counter = 0 # Reset counter for next screen if needed

        elif current_screen == GameScreen.TITLE:
            # Press enter to change to GAMEPLAY screen
            if rl.is_key_pressed(rl.KEY_ENTER) or rl.is_gesture_detected(rl.GESTURE_TAP):
                current_screen = GameScreen.GAMEPLAY

        elif current_screen == GameScreen.GAMEPLAY:
            # Press enter to change to ENDING screen
            if rl.is_key_pressed(rl.KEY_ENTER) or rl.is_gesture_detected(rl.GESTURE_TAP):
                current_screen = GameScreen.ENDING

        elif current_screen == GameScreen.ENDING:
            # Press enter to return to TITLE screen
            if rl.is_key_pressed(rl.KEY_ENTER) or rl.is_gesture_detected(rl.GESTURE_TAP):
                current_screen = GameScreen.TITLE

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        if current_screen == GameScreen.LOGO:
            rl.draw_text("LOGO SCREEN", 20, 20, 40, rl.LIGHTGRAY)
            rl.draw_text("WAIT for 2 SECONDS...", 290, 220, 20, rl.GRAY)

        elif current_screen == GameScreen.TITLE:
            rl.draw_rectangle(0, 0, screen_width, screen_height, rl.GREEN)
            rl.draw_text("TITLE SCREEN", 20, 20, 40, rl.DARKGREEN)
            rl.draw_text("PRESS ENTER or TAP to JUMP to GAMEPLAY SCREEN", 120, 220, 20, rl.DARKGREEN)

        elif current_screen == GameScreen.GAMEPLAY:
            rl.draw_rectangle(0, 0, screen_width, screen_height, rl.PURPLE)
            rl.draw_text("GAMEPLAY SCREEN", 20, 20, 40, rl.MAROON)
            rl.draw_text("PRESS ENTER or TAP to JUMP to ENDING SCREEN", 130, 220, 20, rl.MAROON)

        elif current_screen == GameScreen.ENDING:
            rl.draw_rectangle(0, 0, screen_width, screen_height, rl.BLUE)
            rl.draw_text("ENDING SCREEN", 20, 20, 40, rl.DARKBLUE)
            rl.draw_text("PRESS ENTER or TAP to RETURN to TITLE SCREEN", 120, 220, 20, rl.DARKBLUE)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()  # Close window and OpenGL context

if __name__ == '__main__':
    main()
