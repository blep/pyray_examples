"""raylib [shaders] example - Color palette switch
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3), to test this example
      on OpenGL ES 2.0 platforms (Android, Raspberry Pi, HTML5), use #version 100 shaders
      raylib comes with shaders ready for both versions, check raylib/shaders install folder
Example originally created with raylib 2.5, last time updated with raylib 3.7
Example contributed by Marco Lizza (@MarcoLizza) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Marco Lizza (@MarcoLizza) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

MAX_PALETTES = 3
COLORS_PER_PALETTE = 8
VALUES_PER_COLOR = 3

# Define color palettes
palettes = [
    # 3-BIT RGB
    [
        0, 0, 0,
        255, 0, 0,
        0, 255, 0, 
        0, 0, 255,
        0, 255, 255,
        255, 0, 255,
        255, 255, 0,
        255, 255, 255,
    ],
    # AMMO-8 (GameBoy-like)
    [
        4, 12, 6,
        17, 35, 24,
        30, 58, 41,
        48, 93, 66,
        77, 128, 97,
        137, 162, 87,
        190, 220, 127,
        238, 255, 204,
    ],
    # RKBV (2-strip film)
    [
        21, 25, 26,
        138, 76, 88,
        217, 98, 117,
        230, 184, 193,
        69, 107, 115,
        75, 151, 166,
        165, 189, 194,
        255, 245, 247,
    ]
]

palette_text = [
    "3-BIT RGB",
    "AMMO-8 (GameBoy-like)",
    "RKBV (2-strip film)"
]

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - color palette switch")    # Load shader to be used on some parts drawing
    # NOTE 1: Using GLSL 330 shader version, on OpenGL ES 2.0 use GLSL 100 shader version
    # NOTE 2: Defining empty string ("") for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/palette_switch.fs"))

    # Get variable (uniform) location on the shader to connect with the program
    # NOTE: If uniform variable could not be found in the shader, function returns -1
    palette_loc = rl.get_shader_location(shader, "palette")

    current_palette = 0
    line_height = screen_height // COLORS_PER_PALETTE

    rl.set_target_fps(60)                       # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():         # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if rl.is_key_pressed(rl.KEY_RIGHT):
            current_palette += 1
        elif rl.is_key_pressed(rl.KEY_LEFT):
            current_palette -= 1

        if current_palette >= MAX_PALETTES:
            current_palette = 0
        elif current_palette < 0:
            current_palette = MAX_PALETTES - 1

        # Send palette data to the shader to be used on drawing
        # NOTE: We are sending RGB triplets w/o the alpha channel
        # Convert the Python list to a C array of ivec3
        palette_data = rl.ffi.new("int[]", palettes[current_palette])
        rl.set_shader_value_v(shader, palette_loc, palette_data, rl.SHADER_UNIFORM_IVEC3, COLORS_PER_PALETTE)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_shader_mode(shader)

        for i in range(COLORS_PER_PALETTE):
            # Draw horizontal screen-wide rectangles with increasing "palette index"
            # The used palette index is encoded in the RGB components of the pixel
            rl.draw_rectangle(0, line_height*i, rl.get_screen_width(), line_height, rl.Color(i, i, i, 255))

        rl.end_shader_mode()

        rl.draw_text("< >", 10, 10, 30, rl.DARKBLUE)
        rl.draw_text("CURRENT PALETTE:", 60, 15, 20, rl.RAYWHITE)
        rl.draw_text(palette_text[current_palette], 300, 15, 20, rl.RED)

        rl.draw_fps(700, 15)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)       # Unload shader

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()