"""raylib [text] example - Font SDF loading
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 1.3, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import platform

THIS_DIR = Path(__file__).resolve().parent

# Set GLSL version based on platform
if platform.system() == "Windows" or platform.system() == "Linux" or platform.system() == "Darwin":
    GLSL_VERSION = 330
else:   # PLATFORM_ANDROID, PLATFORM_WEB
    GLSL_VERSION = 100

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [text] example - SDF fonts")

    # NOTE: Textures/Fonts MUST be loaded after Window initialization (OpenGL context is required)

    msg = "Signed Distance Fields"

    # Loading file to memory
    file_size = rl.ffi.new("int *")
    file_data = rl.load_file_data(str(THIS_DIR/"resources/anonymous_pro_bold.ttf"), file_size)
    file_size = file_size[0]

    # Default font generation from TTF font
    font_default = rl.Font()
    font_default.baseSize = 16
    font_default.glyphCount = 95

    # Loading font data from memory data
    # Parameters > font size: 16, no glyphs array provided (None), glyphs count: 95 (autogenerate chars array)
    font_default.glyphs = rl.load_font_data(file_data, file_size, 16, None, 95, rl.FONT_DEFAULT)
    
    # Parameters > glyphs count: 95, font size: 16, glyphs padding in image: 4 px, pack method: 0 (default)
    recs = rl.ffi.new("Rectangle **")
    atlas = rl.gen_image_font_atlas(font_default.glyphs, recs, 95, 16, 4, 0)
    font_default.recs = recs[0]
    font_default.texture = rl.load_texture_from_image(atlas)
    rl.unload_image(atlas)

    # SDF font generation from TTF font
    font_sdf = rl.Font()
    font_sdf.baseSize = 16
    font_sdf.glyphCount = 95
    
    # Parameters > font size: 16, no glyphs array provided (None), glyphs count: 0 (defaults to 95)
    font_sdf.glyphs = rl.load_font_data(file_data, file_size, 16, None, 0, rl.FONT_SDF)
    
    # Parameters > glyphs count: 95, font size: 16, glyphs padding in image: 0 px, pack method: 1 (Skyline algorithm)
    recs = rl.ffi.new("Rectangle **")
    atlas = rl.gen_image_font_atlas(font_sdf.glyphs, recs, 95, 16, 0, 1)
    font_sdf.recs = recs[0]
    font_sdf.texture = rl.load_texture_from_image(atlas)
    rl.unload_image(atlas)

    rl.unload_file_data(file_data)      # Free memory from loaded file

    # Load SDF required shader (we use default vertex shader)
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/sdf.fs"))
    rl.set_texture_filter(font_sdf.texture, rl.TEXTURE_FILTER_BILINEAR)    # Required for SDF font

    font_position = rl.Vector2(40, screen_height/2.0 - 50)
    text_size = rl.Vector2(0.0, 0.0)
    font_size = 16.0
    current_font = 0            # 0 - font_default, 1 - font_sdf

    rl.set_target_fps(60)       # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        font_size += rl.get_mouse_wheel_move() * 8.0

        if font_size < 6:
            font_size = 6

        if rl.is_key_down(rl.KEY_SPACE):
            current_font = 1
        else:
            current_font = 0

        if current_font == 0:
            text_size = rl.measure_text_ex(font_default, msg, font_size, 0)
        else:
            text_size = rl.measure_text_ex(font_sdf, msg, font_size, 0)

        font_position.x = rl.get_screen_width()/2 - text_size.x/2
        font_position.y = rl.get_screen_height()/2 - text_size.y/2 + 80

        # Draw
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        if current_font == 1:
            # NOTE: SDF fonts require a custom SDf shader to compute fragment color
            rl.begin_shader_mode(shader)    # Activate SDF font shader
            rl.draw_text_ex(font_sdf, msg, font_position, font_size, 0, rl.BLACK)
            rl.end_shader_mode()            # Activate our default shader for next drawings

            rl.draw_texture(font_sdf.texture, 10, 10, rl.BLACK)
        else:
            rl.draw_text_ex(font_default, msg, font_position, font_size, 0, rl.BLACK)
            rl.draw_texture(font_default.texture, 10, 10, rl.BLACK)

        if current_font == 1:
            rl.draw_text("SDF!", 320, 20, 80, rl.RED)
        else:
            rl.draw_text("default font", 315, 40, 30, rl.GRAY)

        rl.draw_text("FONT SIZE: 16.0", rl.get_screen_width() - 240, 20, 20, rl.DARKGRAY)
        rl.draw_text(f"RENDER SIZE: {font_size:.2f}", rl.get_screen_width() - 240, 50, 20, rl.DARKGRAY)
        rl.draw_text("Use MOUSE WHEEL to SCALE TEXT!", rl.get_screen_width() - 240, 90, 10, rl.DARKGRAY)

        rl.draw_text("HOLD SPACE to USE SDF FONT VERSION!", 340, rl.get_screen_height() - 30, 20, rl.MAROON)

        rl.end_drawing()

    # De-Initialization
    rl.unload_font(font_default)    # Default font unloading
    rl.unload_font(font_sdf)        # SDF font unloading

    rl.unload_shader(shader)        # Unload SDF shader

    rl.close_window()               # Close window and OpenGL context

if __name__ == "__main__":
    main()