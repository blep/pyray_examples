"""raylib [shaders] example - Postprocessing with custom uniform variable
Example complexity rating: [★★☆☆] 2/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3), to test this example
      on OpenGL ES 2.0 platforms (Android, Raspberry Pi, HTML5), use #version 100 shaders
      raylib comes with shaders ready for both versions, check raylib/shaders install folder
Example originally created with raylib 1.3, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - custom uniform variable")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(8.0, 8.0, 8.0)    # Camera position
    camera.target = rl.Vector3(0.0, 1.5, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    model = rl.load_model(str(THIS_DIR/"resources/models/barracks.obj"))                  # Load OBJ model
    texture = rl.load_texture(str(THIS_DIR/"resources/models/barracks_diffuse.png"))      # Load model texture (diffuse map)
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture                    # Set model diffuse texture

    position = rl.Vector3(0.0, 0.0, 0.0)                                                  # Set model position    # Load postprocessing shader
    # NOTE: Defining empty string ("") for vertex shader forces usage of internal default vertex shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/swirl.fs"))

    # Get variable (uniform) location on the shader to connect with the program
    # NOTE: If uniform variable could not be found in the shader, function returns -1
    swirl_center_loc = rl.get_shader_location(shader, "center")

    swirl_center = rl.ffi.new("float[2]", [screen_width/2, screen_height/2])

    # Create a RenderTexture2D to be used for render to texture
    target = rl.load_render_texture(screen_width, screen_height)

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.ffi.addressof(camera), rl.CAMERA_ORBITAL)
        
        mouse_position = rl.get_mouse_position()

        swirl_center[0] = mouse_position.x
        swirl_center[1] = screen_height - mouse_position.y

        # Send new value to the shader to be used on drawing
        rl.set_shader_value(shader, swirl_center_loc, swirl_center, rl.SHADER_UNIFORM_VEC2)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_texture_mode(target)       # Enable drawing to texture
        rl.clear_background(rl.RAYWHITE)    # Clear texture background

        rl.begin_mode_3d(camera)             # Begin 3d mode drawing
        rl.draw_model(model, position, 0.5, rl.WHITE)   # Draw 3d model with texture
        rl.draw_grid(10, 1.0)               # Draw a grid
        rl.end_mode_3d()                     # End 3d mode drawing, returns to orthographic 2d mode

        rl.draw_text("TEXT DRAWN IN RENDER TEXTURE", 200, 10, 30, rl.RED)
        rl.end_texture_mode()               # End drawing to texture (now we have a texture available for next passes)

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)    # Clear screen background

        # Enable shader using the custom uniform
        rl.begin_shader_mode(shader)
        # NOTE: Render texture must be y-flipped due to default OpenGL coordinates (left-bottom)
        rl.draw_texture_rec(
            target.texture, 
            rl.Rectangle(0, 0, target.texture.width, -target.texture.height),
            rl.Vector2(0, 0),
            rl.WHITE
        )
        rl.end_shader_mode()

        # Draw some 2d text over drawn texture
        rl.draw_text("(c) Barracks 3D model by Alberto Cano", screen_width - 220, screen_height - 20, 10, rl.GRAY)
        rl.draw_fps(10, 10)
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)               # Unload shader
    rl.unload_texture(texture)             # Unload texture
    rl.unload_model(model)                 # Unload model
    rl.unload_render_texture(target)       # Unload render texture

    rl.close_window()                      # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()