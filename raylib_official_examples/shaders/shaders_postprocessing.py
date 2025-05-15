"""raylib [shaders] example - Apply a postprocessing shader to a scene
Example complexity rating: [★★★☆] 3/4
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

# Define postprocessing effect shader types
MAX_POSTPRO_SHADERS = 12

# Enum for the shader types
FX_GRAYSCALE = 0
FX_POSTERIZATION = 1
FX_DREAM_VISION = 2
FX_PIXELIZER = 3
FX_CROSS_HATCHING = 4
FX_CROSS_STITCHING = 5
FX_PREDATOR_VIEW = 6
FX_SCANLINES = 7
FX_FISHEYE = 8
FX_SOBEL = 9
FX_BLOOM = 10
FX_BLUR = 11

# Text to display for each shader
postpro_shader_text = [
    "GRAYSCALE",
    "POSTERIZATION",
    "DREAM_VISION",
    "PIXELIZER",
    "CROSS_HATCHING",
    "CROSS_STITCHING",
    "PREDATOR_VIEW",
    "SCANLINES",
    "FISHEYE",
    "SOBEL",
    "BLOOM",
    "BLUR"
]

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)      # Enable Multi Sampling Anti Aliasing 4x (if available)

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - postprocessing shader")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(2.0, 3.0, 2.0)    # Camera position
    camera.target = rl.Vector3(0.0, 1.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    model = rl.load_model(str(THIS_DIR/"resources/models/church.obj"))                 # Load OBJ model
    texture = rl.load_texture(str(THIS_DIR/"resources/models/church_diffuse.png"))     # Load model texture (diffuse map)
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture                 # Set model diffuse texture

    position = rl.Vector3(0.0, 0.0, 0.0)            # Set model position

    # Load all postpro shaders
    # NOTE 1: All postpro shader use the base vertex shader (DEFAULT_VERTEX_SHADER)
    # NOTE 2: We load the correct shader depending on GLSL version
    shaders = [None] * MAX_POSTPRO_SHADERS    # NOTE: Defining empty string ("") for vertex shader forces usage of internal default vertex shader
    shaders[FX_GRAYSCALE] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/grayscale.fs"))
    shaders[FX_POSTERIZATION] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/posterization.fs"))
    shaders[FX_DREAM_VISION] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/dream_vision.fs"))
    shaders[FX_PIXELIZER] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/pixelizer.fs"))
    shaders[FX_CROSS_HATCHING] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/cross_hatching.fs"))
    shaders[FX_CROSS_STITCHING] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/cross_stitching.fs"))
    shaders[FX_PREDATOR_VIEW] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/predator.fs"))
    shaders[FX_SCANLINES] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/scanlines.fs"))
    shaders[FX_FISHEYE] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/fisheye.fs"))
    shaders[FX_SOBEL] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/sobel.fs"))
    shaders[FX_BLOOM] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/bloom.fs"))
    shaders[FX_BLUR] = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/blur.fs"))

    current_shader = FX_GRAYSCALE

    # Create a RenderTexture2D to be used for render to texture
    target = rl.load_render_texture(screen_width, screen_height)

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():     # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.ffi.addressof(camera), rl.CAMERA_ORBITAL)

        if rl.is_key_pressed(rl.KEY_RIGHT):
            current_shader += 1
        elif rl.is_key_pressed(rl.KEY_LEFT):
            current_shader -= 1

        if current_shader >= MAX_POSTPRO_SHADERS:
            current_shader = 0
        elif current_shader < 0:
            current_shader = MAX_POSTPRO_SHADERS - 1
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_texture_mode(target)       # Enable drawing to texture
        rl.clear_background(rl.RAYWHITE)    # Clear texture background

        rl.begin_mode_3d(camera)            # Begin 3d mode drawing
        rl.draw_model(model, position, 0.1, rl.WHITE)   # Draw 3d model with texture
        rl.draw_grid(10, 1.0)              # Draw a grid
        rl.end_mode_3d()                    # End 3d mode drawing, returns to orthographic 2d mode
        rl.end_texture_mode()               # End drawing to texture (now we have a texture available for next passes)
        
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)    # Clear screen background

        # Render generated texture using selected postprocessing shader
        rl.begin_shader_mode(shaders[current_shader])
            # NOTE: Render texture must be y-flipped due to default OpenGL coordinates (left-bottom)
        rl.draw_texture_rec(
            target.texture,
            rl.Rectangle(0, 0, target.texture.width, -target.texture.height),
            rl.Vector2(0, 0),
            rl.WHITE
        )
        rl.end_shader_mode()

        # Draw 2d shapes and text over drawn texture
        rl.draw_rectangle(0, 9, 580, 30, rl.fade(rl.LIGHTGRAY, 0.7))

        rl.draw_text("(c) Church 3D model by Alberto Cano", screen_width - 200, screen_height - 20, 10, rl.GRAY)
        rl.draw_text("CURRENT POSTPRO SHADER:", 10, 15, 20, rl.BLACK)
        rl.draw_text(postpro_shader_text[current_shader], 330, 15, 20, rl.RED)
        rl.draw_text("< >", 540, 10, 30, rl.DARKBLUE)
        rl.draw_fps(700, 15)
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    # Unload all postpro shaders
    for i in range(MAX_POSTPRO_SHADERS):
        rl.unload_shader(shaders[i])

    rl.unload_texture(texture)         # Unload texture
    rl.unload_model(model)             # Unload model
    rl.unload_render_texture(target)   # Unload render texture

    rl.close_window()                  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()