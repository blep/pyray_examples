"""raylib [shaders] example - Texture Waves
Example complexity rating: [★★☆☆] 2/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3), to test this example
      on OpenGL ES 2.0 platforms (Android, Raspberry Pi, HTML5), use #version 100 shaders
      raylib comes with shaders ready for both versions, check raylib/shaders install folder
Example originally created with raylib 2.5, last time updated with raylib 3.7
Example contributed by Anata (@anatagawa) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Anata (@anatagawa) and Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - texture waves")

    # Load texture texture to apply shaders
    texture = rl.load_texture(str(THIS_DIR/"resources/space.png"))

    # Load shader and setup location points and values
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/wave.fs"))

    seconds_loc = rl.get_shader_location(shader, "seconds")
    freq_x_loc = rl.get_shader_location(shader, "freqX")
    freq_y_loc = rl.get_shader_location(shader, "freqY")
    amp_x_loc = rl.get_shader_location(shader, "ampX")
    amp_y_loc = rl.get_shader_location(shader, "ampY")
    speed_x_loc = rl.get_shader_location(shader, "speedX")
    speed_y_loc = rl.get_shader_location(shader, "speedY")

    # Shader uniform values that can be updated at any time
    freq_x = 25.0
    freq_y = 25.0
    amp_x = 5.0
    amp_y = 5.0
    speed_x = 8.0
    speed_y = 8.0

    screen_size = rl.ffi.new("float[2]", [float(rl.get_screen_width()), float(rl.get_screen_height())])
    rl.set_shader_value(shader, rl.get_shader_location(shader, "size"), screen_size, rl.SHADER_UNIFORM_VEC2)
    rl.set_shader_value(shader, freq_x_loc, rl.ffi.new("float *", freq_x), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, freq_y_loc, rl.ffi.new("float *", freq_y), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, amp_x_loc, rl.ffi.new("float *", amp_x), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, amp_y_loc, rl.ffi.new("float *", amp_y), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, speed_x_loc, rl.ffi.new("float *", speed_x), rl.SHADER_UNIFORM_FLOAT)
    rl.set_shader_value(shader, speed_y_loc, rl.ffi.new("float *", speed_y), rl.SHADER_UNIFORM_FLOAT)

    seconds = 0.0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    # -------------------------------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        seconds += rl.get_frame_time()

        rl.set_shader_value(shader, seconds_loc, rl.ffi.new("float *", seconds), rl.SHADER_UNIFORM_FLOAT)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_shader_mode(shader)

        rl.draw_texture(texture, 0, 0, rl.WHITE)
        rl.draw_texture(texture, texture.width, 0, rl.WHITE)

        rl.end_shader_mode()

        rl.draw_text("WAVE SHADER", 10, 10, 20, rl.RED)
        rl.draw_text("(c) Space texture by spaceport7.com", 10, 430, 10, rl.RAYWHITE)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture)
    rl.unload_shader(shader)

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()