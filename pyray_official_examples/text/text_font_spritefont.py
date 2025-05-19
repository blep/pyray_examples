"""raylib [text] example - Sprite font loading
Example complexity rating: [★☆☆☆] 1/4
NOTE: Sprite fonts should be generated following this conventions:
  - Characters must be ordered starting with character 32 (Space)
  - Every character must be contained within the same Rectangle height
  - Every character and every line must be separated by the same distance (margin/padding)
  - Rectangles must be defined by a MAGENTA color background
Following those constraints, a font can be provided just by an image,
this is quite handy to avoid additional font descriptor files (like BMFonts use).
Example originally created with raylib 1.0, last time updated with raylib 1.0
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
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - sprite font loading")

    msg1 = "THIS IS A custom SPRITE FONT..."
    msg2 = "...and this is ANOTHER CUSTOM font..."
    msg3 = "...and a THIRD one! GREAT! :D"

    # NOTE: Textures/Fonts MUST be loaded after Window initialization (OpenGL context is required)
    font1 = rl.load_font(str(THIS_DIR/"resources/custom_mecha.png"))          # Font loading
    font2 = rl.load_font(str(THIS_DIR/"resources/custom_alagard.png"))        # Font loading
    font3 = rl.load_font(str(THIS_DIR/"resources/custom_jupiter_crash.png"))  # Font loading

    font_position1 = rl.Vector2(
        screen_width/2.0 - rl.measure_text_ex(font1, msg1, float(font1.baseSize), -3).x/2,
        screen_height/2.0 - font1.baseSize/2.0 - 80.0
    )

    font_position2 = rl.Vector2(
        screen_width/2.0 - rl.measure_text_ex(font2, msg2, float(font2.baseSize), -2.0).x/2.0,
        screen_height/2.0 - font2.baseSize/2.0 - 10.0
    )

    font_position3 = rl.Vector2(
        screen_width/2.0 - rl.measure_text_ex(font3, msg3, float(font3.baseSize), 2.0).x/2.0,
        screen_height/2.0 - font3.baseSize/2.0 + 50.0
    )

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        # TODO: Update variables here...

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text_ex(font1, msg1, font_position1, float(font1.baseSize), -3, rl.WHITE)
        rl.draw_text_ex(font2, msg2, font_position2, float(font2.baseSize), -2, rl.WHITE)
        rl.draw_text_ex(font3, msg3, font_position3, float(font3.baseSize), 2, rl.WHITE)

        rl.end_drawing()

    # De-Initialization
    rl.unload_font(font1)      # Font unloading
    rl.unload_font(font2)      # Font unloading
    rl.unload_font(font3)      # Font unloading

    rl.close_window()          # Close window and OpenGL context

if __name__ == "__main__":
    main()