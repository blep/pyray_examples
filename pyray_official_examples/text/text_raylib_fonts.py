"""raylib [text] example - raylib fonts loading
Example complexity rating: [★☆☆☆] 1/4
NOTE: raylib is distributed with some free to use fonts (even for commercial pourposes!)
      To view details and credits for those fonts, check raylib license file
Example originally created with raylib 1.7, last time updated with raylib 3.7
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

MAX_FONTS = 8

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - raylib fonts")

    # NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
    fonts = [None] * MAX_FONTS

    fonts[0] = rl.load_font(str(THIS_DIR/"resources/fonts/alagard.png"))
    fonts[1] = rl.load_font(str(THIS_DIR/"resources/fonts/pixelplay.png"))
    fonts[2] = rl.load_font(str(THIS_DIR/"resources/fonts/mecha.png"))
    fonts[3] = rl.load_font(str(THIS_DIR/"resources/fonts/setback.png"))
    fonts[4] = rl.load_font(str(THIS_DIR/"resources/fonts/romulus.png"))
    fonts[5] = rl.load_font(str(THIS_DIR/"resources/fonts/pixantiqua.png"))
    fonts[6] = rl.load_font(str(THIS_DIR/"resources/fonts/alpha_beta.png"))
    fonts[7] = rl.load_font(str(THIS_DIR/"resources/fonts/jupiter_crash.png"))

    messages = [
        "ALAGARD FONT designed by Hewett Tsoi",
        "PIXELPLAY FONT designed by Aleksander Shevchuk",
        "MECHA FONT designed by Captain Falcon",
        "SETBACK FONT designed by Brian Kent (AEnigma)",
        "ROMULUS FONT designed by Hewett Tsoi",
        "PIXANTIQUA FONT designed by Gerhard Grossmann",
        "ALPHA_BETA FONT designed by Brian Kent (AEnigma)",
        "JUPITER_CRASH FONT designed by Brian Kent (AEnigma)"
    ]

    spacings = [2, 4, 8, 4, 3, 4, 4, 1]

    positions = [rl.Vector2(0, 0)] * MAX_FONTS

    for i in range(MAX_FONTS):
        positions[i].x = screen_width/2.0 - rl.measure_text_ex(fonts[i], messages[i], fonts[i].baseSize*2.0, float(spacings[i])).x/2.0
        positions[i].y = 60.0 + fonts[i].baseSize + 45.0*i

    # Small Y position corrections
    positions[3].y += 8
    positions[4].y += 2
    positions[7].y -= 8

    colors = [rl.MAROON, rl.ORANGE, rl.DARKGREEN, rl.DARKBLUE, rl.DARKPURPLE, rl.LIME, rl.GOLD, rl.RED]

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # TODO: Update your variables here

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("free fonts included with raylib", 250, 20, 20, rl.DARKGRAY)
        rl.draw_line(220, 50, 590, 50, rl.DARKGRAY)

        for i in range(MAX_FONTS):
            rl.draw_text_ex(fonts[i], messages[i], positions[i], fonts[i].baseSize*2.0, float(spacings[i]), colors[i])

        rl.end_drawing()

    # De-Initialization
    # Fonts unloading
    for i in range(MAX_FONTS):
        rl.unload_font(fonts[i])

    rl.close_window()  # Close window and OpenGL context

if __name__ == "__main__":
    main()