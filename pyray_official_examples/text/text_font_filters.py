"""raylib [text] example - Font filters
Example complexity rating: [★★☆☆] 2/4
NOTE: After font loading, font texture atlas filter could be configured for a softer
display of the font when scaling it to different sizes, that way, it's not required
to generate multiple fonts at multiple sizes (as long as the scaling is not very different)
Example originally created with raylib 1.3, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - font filters")

    msg = "Loaded Font"

    # NOTE: Textures/Fonts MUST be loaded after Window initialization (OpenGL context is required)

    # TTF Font loading with custom generation parameters
    font = rl.load_font_ex(str(THIS_DIR/"resources/KAISG.ttf"), 96, None, 0)

    # Generate mipmap levels to use trilinear filtering
    # NOTE: On 2D drawing it won't be noticeable, it looks like FILTER_BILINEAR
    rl.gen_texture_mipmaps(rl.ffi.addressof(font.texture))

    font_size = float(font.baseSize)
    font_position = rl.Vector2(40.0, screen_height/2.0 - 80.0)
    text_size = rl.Vector2(0.0, 0.0)

    # Setup texture scaling filter
    rl.set_texture_filter(font.texture, rl.TEXTURE_FILTER_POINT)
    current_font_filter = 0      # TEXTURE_FILTER_POINT

    rl.set_target_fps(60)        # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        font_size += rl.get_mouse_wheel_move() * 4.0

        # Choose font texture filter method
        if rl.is_key_pressed(rl.KEY_ONE):
            rl.set_texture_filter(font.texture, rl.TEXTURE_FILTER_POINT)
            current_font_filter = 0
        elif rl.is_key_pressed(rl.KEY_TWO):
            rl.set_texture_filter(font.texture, rl.TEXTURE_FILTER_BILINEAR)
            current_font_filter = 1
        elif rl.is_key_pressed(rl.KEY_THREE):
            # NOTE: Trilinear filter won't be noticed on 2D drawing
            rl.set_texture_filter(font.texture, rl.TEXTURE_FILTER_TRILINEAR)
            current_font_filter = 2

        text_size = rl.measure_text_ex(font, msg, font_size, 0)

        if rl.is_key_down(rl.KEY_LEFT):
            font_position.x -= 10
        elif rl.is_key_down(rl.KEY_RIGHT):
            font_position.x += 10

        # Load a dropped TTF file dynamically (at current fontSize)
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()

            # NOTE: We only support first ttf file dropped
            if rl.is_file_extension(dropped_files.paths[0], ".ttf"):
                rl.unload_font(font)
                font = rl.load_font_ex(dropped_files.paths[0], int(font_size), None, 0)
            
            rl.unload_dropped_files(dropped_files)    # Unload filepaths from memory

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_text("Use mouse wheel to change font size", 20, 20, 10, rl.GRAY)
        rl.draw_text("Use KEY_RIGHT and KEY_LEFT to move text", 20, 40, 10, rl.GRAY)
        rl.draw_text("Use 1, 2, 3 to change texture filter", 20, 60, 10, rl.GRAY)
        rl.draw_text("Drop a new TTF font for dynamic loading", 20, 80, 10, rl.DARKGRAY)

        rl.draw_text_ex(font, msg, font_position, font_size, 0, rl.BLACK)

        # TODO: It seems texSize measurement is not accurate due to chars offsets...
        #rl.draw_rectangle_lines(int(font_position.x), int(font_position.y), int(text_size.x), int(text_size.y), rl.RED)

        rl.draw_rectangle(0, screen_height - 80, screen_width, 80, rl.LIGHTGRAY)
        rl.draw_text(f"Font size: {font_size:.2f}", 20, screen_height - 50, 10, rl.DARKGRAY)
        rl.draw_text(f"Text size: [{text_size.x:.2f}, {text_size.y:.2f}]", 20, screen_height - 30, 10, rl.DARKGRAY)
        rl.draw_text("CURRENT TEXTURE FILTER:", 250, 400, 20, rl.GRAY)

        if current_font_filter == 0:
            rl.draw_text("POINT", 570, 400, 20, rl.BLACK)
        elif current_font_filter == 1:
            rl.draw_text("BILINEAR", 570, 400, 20, rl.BLACK)
        elif current_font_filter == 2:
            rl.draw_text("TRILINEAR", 570, 400, 20, rl.BLACK)

        rl.end_drawing()

    # De-Initialization
    rl.unload_font(font)           # Font unloading
    rl.close_window()              # Close window and OpenGL context

if __name__ == "__main__":
    main()