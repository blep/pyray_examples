"""raylib [shaders] example - Texture drawing
Example complexity rating: [★★☆☆] 2/4
NOTE: This example illustrates how to draw into a blank texture using a shader
Example originally created with raylib 2.0, last time updated with raylib 3.7
Example contributed by Michał Ciesielski (@ciessielski) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Michał Ciesielski (@ciessielski) and Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - texture drawing")

    im_blank = rl.gen_image_color(1024, 1024, rl.BLANK)
    texture = rl.load_texture_from_image(im_blank)  # Load blank texture to fill on shader
    rl.unload_image(im_blank)

    # NOTE: Using GLSL 330 shader version, on OpenGL ES 2.0 use GLSL 100 shader version
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/cubes_panning.fs"))

    time = 0.0
    time_loc = rl.get_shader_location(shader, "uTime")
    rl.set_shader_value(shader, time_loc, rl.ffi.new("float *", time), rl.SHADER_UNIFORM_FLOAT)

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    # -------------------------------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        time = rl.get_time()
        rl.set_shader_value(shader, time_loc, rl.ffi.new("float *", time), rl.SHADER_UNIFORM_FLOAT)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_shader_mode(shader)    # Enable our custom shader for next shapes/textures drawings
        rl.draw_texture(texture, 0, 0, rl.WHITE)  # Drawing BLANK texture, all magic happens on shader
        rl.end_shader_mode()            # Disable our custom shader, return to default shader

        rl.draw_text("BACKGROUND is PAINTED and ANIMATED on SHADER!", 10, 10, 20, rl.MAROON)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)
    rl.unload_texture(texture)

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()