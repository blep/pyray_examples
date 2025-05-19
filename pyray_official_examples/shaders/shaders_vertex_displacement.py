"""raylib [shaders] example - Vertex displacement
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.0, last time updated with raylib 4.5
Example contributed by Alex ZH (@ZzzhHe) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Alex ZH (@ZzzhHe)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

from rlights import LIGHT_POINT, create_light  # Import the lights module

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

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - vertex displacement")

    # set up camera
    camera = rl.Camera3D()
    camera.position = rl.Vector3(20.0, 5.0, -20.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 60.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    # Load vertex and fragment shaders
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/vertex_displacement.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/vertex_displacement.fs")
    )
    
    # Load perlin noise texture
    perlin_noise_image = rl.gen_image_perlin_noise(512, 512, 0, 0, 1.0)
    perlin_noise_map = rl.load_texture_from_image(perlin_noise_image)
    rl.unload_image(perlin_noise_image)

    # Set shader uniform location
    perlin_noise_map_loc = rl.get_shader_location(shader, "perlinNoiseMap")
    rl.rl_enable_shader(shader.id)
    rl.rl_active_texture_slot(1)
    rl.rl_enable_texture(perlin_noise_map.id)
    rl.rl_set_uniform_sampler(perlin_noise_map_loc, 1)
    
    # Create a plane mesh and model
    plane_mesh = rl.gen_mesh_plane(50, 50, 50, 50)
    plane_model = rl.load_model_from_mesh(plane_mesh)
    # Set plane model material
    plane_model.materials[0].shader = shader

    time = 0.0

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FREE)  # Update camera

        time += rl.get_frame_time()  # Update time variable
        rl.set_shader_value(shader, rl.get_shader_location(shader, "time"), rl.ffi.new("float *", time), rl.SHADER_UNIFORM_FLOAT)  # Send time value to shader

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.begin_shader_mode(shader)
        # Draw plane model
        rl.draw_model(plane_model, rl.Vector3(0.0, 0.0, 0.0), 1.0, rl.Color(255, 255, 255, 255))
        rl.end_shader_mode()

        rl.end_mode_3d()

        rl.draw_text("Vertex displacement", 10, 10, 20, rl.DARKGRAY)
        rl.draw_fps(10, 40)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)
    rl.unload_model(plane_model)
    rl.unload_texture(perlin_noise_map)

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()