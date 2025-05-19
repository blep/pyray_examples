"""raylib [shaders] example - Multiple sample2D with default batch system
Example complexity rating: [★★☆☆] 2/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3), to test this example
      on OpenGL ES 2.0 platforms (Android, Raspberry Pi, HTML5), use #version 100 shaders
      raylib comes with shaders ready for both versions, check raylib/shaders install folder
Example originally created with raylib 3.5, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib - multiple sample2D")

    im_red = rl.gen_image_color(800, 450, rl.Color(255, 0, 0, 255))
    tex_red = rl.load_texture_from_image(im_red)
    rl.unload_image(im_red)

    im_blue = rl.gen_image_color(800, 450, rl.Color(0, 0, 255, 255))
    tex_blue = rl.load_texture_from_image(im_blue)
    rl.unload_image(im_blue)

    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/color_mix.fs"))

    # Get an additional sampler2D location to be enabled on drawing
    tex_blue_loc = rl.get_shader_location(shader, "texture1")

    # Get shader uniform for divider
    divider_loc = rl.get_shader_location(shader, "divider")
    divider_value = 0.5

    rl.set_target_fps(60)                           # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():                # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if rl.is_key_down(rl.KEY_RIGHT):
            divider_value += 0.01
        elif rl.is_key_down(rl.KEY_LEFT):
            divider_value -= 0.01

        if divider_value < 0.0:
            divider_value = 0.0
        elif divider_value > 1.0:
            divider_value = 1.0

        rl.set_shader_value(shader, divider_loc, rl.ffi.new("float *", divider_value), rl.SHADER_UNIFORM_FLOAT)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_shader_mode(shader)

        # WARNING: Additional samplers are enabled for all draw calls in the batch,
        # EndShaderMode() forces batch drawing and consequently resets active textures
        # to let other sampler2D to be activated on consequent drawings (if required)
        rl.set_shader_value_texture(shader, tex_blue_loc, tex_blue)

        # We are drawing tex_red using default sampler2D texture0 but
        # an additional texture units is enabled for tex_blue (sampler2D texture1)
        rl.draw_texture(tex_red, 0, 0, rl.WHITE)

        rl.end_shader_mode()

        rl.draw_text("Use KEY_LEFT/KEY_RIGHT to move texture mixing in shader!", 80, rl.get_screen_height() - 40, 20, rl.RAYWHITE)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)       # Unload shader
    rl.unload_texture(tex_red)     # Unload texture
    rl.unload_texture(tex_blue)    # Unload texture

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()