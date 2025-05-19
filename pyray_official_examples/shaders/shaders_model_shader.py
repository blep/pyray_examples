"""raylib [shaders] example - Model shader
Example complexity rating: [★★☆☆] 2/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3), to test this example
      on OpenGL ES 2.0 platforms (Android, Raspberry Pi, HTML5), use #version 100 shaders
      raylib comes with shaders ready for both versions, check raylib/shaders install folder
Example originally created with raylib 1.3, last time updated with raylib 3.7
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

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

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)      # Enable Multi Sampling Anti Aliasing 4x (if available)

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - model shader")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(4.0, 4.0, 4.0)    # Camera position
    camera.target = rl.Vector3(0.0, 1.0, -1.0)     # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    model = rl.load_model(str(THIS_DIR/"resources/models/watermill.obj"))                   # Load OBJ model
    texture = rl.load_texture(str(THIS_DIR/"resources/models/watermill_diffuse.png"))       # Load model texture    # Load shader for model
    # NOTE: Defining empty string ("") for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/grayscale.fs"))

    model.materials[0].shader = shader                 # Set shader effect to 3d model
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture  # Bind texture to model

    position = rl.Vector3(0.0, 0.0, 0.0)     # Set model position

    rl.disable_cursor()                     # Limit cursor to relative movement inside the window
    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():     # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.ffi.addressof(camera), rl.CAMERA_FREE)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_model(model, position, 0.2, rl.WHITE)   # Draw 3d model with texture

        rl.draw_grid(10, 1.0)     # Draw a grid

        rl.end_mode_3d()

        rl.draw_text("(c) Watermill 3D model by Alberto Cano", screen_width - 210, screen_height - 20, 10, rl.GRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)       # Unload shader
    rl.unload_texture(texture)     # Unload texture
    rl.unload_model(model)         # Unload model

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()