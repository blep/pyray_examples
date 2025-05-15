"""raylib [shaders] example - Raymarching shapes generation
Example complexity rating: [★★★★] 4/4
NOTE: This example requires raylib OpenGL 3.3 for shaders support and only #version 330
      is currently supported. OpenGL ES 2.0 platforms are not supported at the moment.
Example originally created with raylib 2.0, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Ramon Santamaria (@raysan5)

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

    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - raymarching shapes")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(2.5, 2.5, 3.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.7)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 65.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load raymarching shader
    # NOTE: Defining "" (empty string) for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/raymarching.fs"))

    # Get shader locations for required uniforms
    view_eye_loc = rl.get_shader_location(shader, "viewEye")
    view_center_loc = rl.get_shader_location(shader, "viewCenter")
    run_time_loc = rl.get_shader_location(shader, "runTime")
    resolution_loc = rl.get_shader_location(shader, "resolution")

    resolution = rl.ffi.new("float[2]", [float(screen_width), float(screen_height)])
    rl.set_shader_value(shader, resolution_loc, resolution, rl.SHADER_UNIFORM_VEC2)

    run_time = 0.0

    rl.disable_cursor()                    # Limit cursor to relative movement inside the window
    rl.set_target_fps(60)                  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        camera_pos = rl.ffi.new("float[3]", [camera.position.x, camera.position.y, camera.position.z])
        camera_target = rl.ffi.new("float[3]", [camera.target.x, camera.target.y, camera.target.z])

        delta_time = rl.get_frame_time()
        run_time += delta_time

        # Set shader required uniform values
        rl.set_shader_value(shader, view_eye_loc, camera_pos, rl.SHADER_UNIFORM_VEC3)
        rl.set_shader_value(shader, view_center_loc, camera_target, rl.SHADER_UNIFORM_VEC3)
        rl.set_shader_value(shader, run_time_loc, rl.ffi.new("float *", run_time), rl.SHADER_UNIFORM_FLOAT)

        # Check if screen is resized
        if rl.is_window_resized():
            resolution[0] = float(rl.get_screen_width())
            resolution[1] = float(rl.get_screen_height())
            rl.set_shader_value(shader, resolution_loc, resolution, rl.SHADER_UNIFORM_VEC2)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        # We only draw a white full-screen rectangle,
        # frame is generated in shader using raymarching
        rl.begin_shader_mode(shader)
        rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.WHITE)
        rl.end_shader_mode()

        rl.draw_text("(c) Raymarching shader by Iñigo Quilez. MIT License.", rl.get_screen_width() - 280, rl.get_screen_height() - 20, 10, rl.BLACK)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)           # Unload shader

    rl.close_window()                  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()