"""raylib [shaders] example - texture tiling
Example complexity rating: [★★☆☆] 2/4
Example demonstrates how to tile a texture on a 3D model using raylib.
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by Luis Almeida (@luis605) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Luis Almeida (@luis605)

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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - texture tiling")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(4.0, 4.0, 4.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.5, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load a cube model
    cube = rl.gen_mesh_cube(1.0, 1.0, 1.0)
    model = rl.load_model_from_mesh(cube)
    
    # Load a texture and assign to cube model
    texture = rl.load_texture(str(THIS_DIR/"resources/cubicmap_atlas.png"))
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture

    # Set the texture tiling using a shader
    tiling = rl.ffi.new("float[2]", [3.0, 3.0])
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/tiling.fs"))
    rl.set_shader_value(shader, rl.get_shader_location(shader, "tiling"), tiling, rl.SHADER_UNIFORM_VEC2)
    model.materials[0].shader = shader

    rl.disable_cursor()                    # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)                  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FREE)

        if rl.is_key_pressed(rl.KEY_Z):
            camera.target = rl.Vector3(0.0, 0.5, 0.0)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
        
        rl.begin_shader_mode(shader)
        rl.draw_model(model, rl.Vector3(0.0, 0.0, 0.0), 2.0, rl.WHITE)
        rl.end_shader_mode()

        rl.draw_grid(10, 1.0)
            
        rl.end_mode_3d()

        rl.draw_text("Use mouse to rotate the camera", 10, 10, 20, rl.DARKGRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model)         # Unload model
    rl.unload_shader(shader)       # Unload shader
    rl.unload_texture(texture)     # Unload texture

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
    
if __name__ == "__main__":
    main()