"""raylib [shaders] example - Hot reloading
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires raylib OpenGL 3.3 for shaders support and only #version 330
      is currently supported. OpenGL ES 2.0 platforms are not supported at the moment.
Example originally created with raylib 3.0, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import time
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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - hot reloading")

    frag_shader_file_name = str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/reload.fs")
    frag_shader_file_mod_time = rl.get_file_mod_time(frag_shader_file_name)

    # Load raymarching shader
    # NOTE: Defining 0 (NULL) for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", frag_shader_file_name)

    # Get shader locations for required uniforms
    resolution_loc = rl.get_shader_location(shader, "resolution")
    mouse_loc = rl.get_shader_location(shader, "mouse")
    time_loc = rl.get_shader_location(shader, "time")

    resolution = rl.ffi.new("float[2]", [screen_width, screen_height])
    rl.set_shader_value(shader, resolution_loc, resolution, rl.SHADER_UNIFORM_VEC2)

    total_time = 0.0
    shader_auto_reloading = False

    rl.set_target_fps(60)                       # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():            # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        total_time += rl.get_frame_time()
        mouse = rl.get_mouse_position()
        mouse_pos = rl.ffi.new("float[2]", [mouse.x, mouse.y])

        # Set shader required uniform values
        rl.set_shader_value(shader, time_loc, rl.ffi.new("float *", total_time), rl.SHADER_UNIFORM_FLOAT)
        rl.set_shader_value(shader, mouse_loc, mouse_pos, rl.SHADER_UNIFORM_VEC2)

        # Hot shader reloading
        if shader_auto_reloading or (rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT)):
            current_frag_shader_mod_time = rl.get_file_mod_time(frag_shader_file_name)

            # Check if shader file has been modified
            if current_frag_shader_mod_time != frag_shader_file_mod_time:
                # Try reloading updated shader
                updated_shader = rl.load_shader("", frag_shader_file_name)

                if updated_shader.id != rl.rl_get_shader_id_default():      # It was correctly loaded
                    rl.unload_shader(shader)
                    shader = updated_shader

                    # Get shader locations for required uniforms
                    resolution_loc = rl.get_shader_location(shader, "resolution")
                    mouse_loc = rl.get_shader_location(shader, "mouse")
                    time_loc = rl.get_shader_location(shader, "time")

                    # Reset required uniforms
                    rl.set_shader_value(shader, resolution_loc, resolution, rl.SHADER_UNIFORM_VEC2)

                frag_shader_file_mod_time = current_frag_shader_mod_time

        if rl.is_key_pressed(rl.KEY_A):
            shader_auto_reloading = not shader_auto_reloading
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        # We only draw a white full-screen rectangle, frame is generated in shader
        rl.begin_shader_mode(shader)
        rl.draw_rectangle(0, 0, screen_width, screen_height, rl.WHITE)
        rl.end_shader_mode()

        rl.draw_text(f"PRESS [A] to TOGGLE SHADER AUTOLOADING: {'AUTO' if shader_auto_reloading else 'MANUAL'}", 
                     10, 10, 10, rl.RED if shader_auto_reloading else rl.BLACK)
        
        if not shader_auto_reloading:
            rl.draw_text("MOUSE CLICK to SHADER RE-LOADING", 10, 30, 10, rl.BLACK)

        shader_mod_time_str = time.asctime(time.localtime(frag_shader_file_mod_time))
        rl.draw_text(f"Shader last modification: {shader_mod_time_str}", 10, 430, 10, rl.BLACK)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)           # Unload shader

    rl.close_window()                  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()