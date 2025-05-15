"""raylib [shaders] example - Apply an shdrOutline to a texture
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
Example originally created with raylib 4.0, last time updated with raylib 4.0
Example contributed by Samuel Skiff (@GoldenThumbs) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Samuel SKiff (@GoldenThumbs) and Ramon Santamaria (@raysan5)

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

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - Apply an outline to a texture")

    texture = rl.load_texture(str(THIS_DIR/"resources/fudesumi.png"))

    shdr_outline = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/outline.fs"))

    outline_size = 2.0
    outline_color = rl.ffi.new("float[4]", [1.0, 0.0, 0.0, 1.0])     # Normalized RED color
    texture_size = rl.ffi.new("float[2]", [texture.width, texture.height])

    # Get shader locations
    outline_size_loc = rl.get_shader_location(shdr_outline, "outlineSize")
    outline_color_loc = rl.get_shader_location(shdr_outline, "outlineColor")
    texture_size_loc = rl.get_shader_location(shdr_outline, "textureSize")

    # Set shader values (they can be changed later)
    rl.set_shader_value(shdr_outline, outline_size_loc, rl.ffi.new("float *", outline_size), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shdr_outline, outline_color_loc, outline_color, rl.SHADER_UNIFORM_VEC4)
    rl.set_shader_value(shdr_outline, texture_size_loc, texture_size, rl.SHADER_UNIFORM_VEC2)

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        outline_size += rl.get_mouse_wheel_move()
        if outline_size < 1.0:
            outline_size = 1.0

        rl.set_shader_value(shdr_outline, outline_size_loc, rl.ffi.new("float *", outline_size), rl.SHADER_UNIFORM_FLOAT)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_shader_mode(shdr_outline)

        rl.draw_texture(texture, rl.get_screen_width()//2 - texture.width//2, -30, rl.WHITE)

        rl.end_shader_mode()

        rl.draw_text("Shader-based\ntexture\noutline", 10, 10, 20, rl.GRAY)
        rl.draw_text("Scroll mouse wheel to\nchange outline size", 10, 72, 20, rl.GRAY)
        rl.draw_text(f"Outline size: {int(outline_size)} px", 10, 120, 20, rl.MAROON)

        rl.draw_fps(710, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture)
    rl.unload_shader(shdr_outline)

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()