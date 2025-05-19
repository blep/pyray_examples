"""raylib [shaders] example - Simple shader mask
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 3.7
Example contributed by Chris Camacho (@chriscamacho) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Chris Camacho (@chriscamacho) and Ramon Santamaria (@raysan5)
After a model is loaded it has a default material, this material can be
modified in place rather than creating one from scratch...
While all of the maps have particular names, they can be used for any purpose
except for three maps that are applied as cubic maps (see below)

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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - simple shader mask")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 1.0, 2.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Define our three models to show the shader on
    torus = rl.gen_mesh_torus(0.3, 1, 16, 32)
    model1 = rl.load_model_from_mesh(torus)

    cube = rl.gen_mesh_cube(0.8, 0.8, 0.8)
    model2 = rl.load_model_from_mesh(cube)

    # Generate model to be shaded just to see the gaps in the other two
    sphere = rl.gen_mesh_sphere(1, 16, 16)
    model3 = rl.load_model_from_mesh(sphere)

    # Load the shader
    shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/mask.fs"))

    # Load and apply the diffuse texture (colour map)
    tex_diffuse = rl.load_texture(str(THIS_DIR/"resources/plasma.png"))
    model1.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = tex_diffuse
    model2.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = tex_diffuse

    # Using MATERIAL_MAP_EMISSION as a spare slot to use for 2nd texture
    # NOTE: Don't use MATERIAL_MAP_IRRADIANCE, MATERIAL_MAP_PREFILTER or MATERIAL_MAP_CUBEMAP as they are bound as cube maps
    tex_mask = rl.load_texture(str(THIS_DIR/"resources/mask.png"))
    model1.materials[0].maps[rl.MATERIAL_MAP_EMISSION].texture = tex_mask
    model2.materials[0].maps[rl.MATERIAL_MAP_EMISSION].texture = tex_mask
    shader.locs[rl.SHADER_LOC_MAP_EMISSION] = rl.get_shader_location(shader, "mask")

    # Frame is incremented each frame to animate the shader
    shader_frame = rl.get_shader_location(shader, "frame")

    # Apply the shader to the two models
    model1.materials[0].shader = shader
    model2.materials[0].shader = shader

    frames_counter = 0
    rotation = rl.Vector3(0, 0, 0)           # Model rotation angles

    rl.disable_cursor()                    # Limit cursor to relative movement inside the window
    rl.set_target_fps(60)                  # Set to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)
        
        frames_counter += 1
        rotation.x += 0.01
        rotation.y += 0.005
        rotation.z -= 0.0025

        # Send frames counter to shader for animation
        rl.set_shader_value(shader, shader_frame, rl.ffi.new("int *", frames_counter), rl.SHADER_UNIFORM_INT)

        # Rotate one of the models
        model1.transform = rl.matrix_rotate_xyz(rotation)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.DARKBLUE)

        rl.begin_mode_3d(camera)

        rl.draw_model(model1, rl.Vector3(0.5, 0.0, 0.0), 1, rl.WHITE)
        rl.draw_model_ex(model2, rl.Vector3(-0.5, 0.0, 0.0), rl.Vector3(1.0, 1.0, 0.0), 50, rl.Vector3(1.0, 1.0, 1.0), rl.WHITE)
        rl.draw_model(model3, rl.Vector3(0.0, 0.0, -1.5), 1, rl.WHITE)
        rl.draw_grid(10, 1.0)       # Draw a grid

        rl.end_mode_3d()

        rl.draw_rectangle(16, 698, rl.measure_text(f"Frame: {frames_counter}", 20) + 8, 42, rl.BLUE)
        rl.draw_text(f"Frame: {frames_counter}", 20, 700, 20, rl.WHITE)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model1)
    rl.unload_model(model2)
    rl.unload_model(model3)

    rl.unload_texture(tex_diffuse)  # Unload default diffuse texture
    rl.unload_texture(tex_mask)     # Unload texture mask

    rl.unload_shader(shader)        # Unload shader

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()