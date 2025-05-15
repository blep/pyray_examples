"""raylib [shaders] example - fog
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3).
Example originally created with raylib 2.5, last time updated with raylib 3.7
Example contributed by Chris Camacho (@chriscamacho) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Chris Camacho (@chriscamacho) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

from rlights import LIGHT_POINT, create_light

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

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)  # Enable Multi Sampling Anti Aliasing 4x (if available)
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - fog")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(2.0, 2.0, 6.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.5, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load models and texture
    model_a = rl.load_model_from_mesh(rl.gen_mesh_torus(0.4, 1.0, 16, 32))
    model_b = rl.load_model_from_mesh(rl.gen_mesh_cube(1.0, 1.0, 1.0))
    model_c = rl.load_model_from_mesh(rl.gen_mesh_sphere(0.5, 32, 32))
    texture = rl.load_texture(str(THIS_DIR/"resources/texel_checker.png"))

    # Assign texture to default model material
    model_a.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture
    model_b.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture
    model_c.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture

    # Load shader and set up some uniforms
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/lighting.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/fog.fs")
    )
    
    shader.locs[rl.SHADER_LOC_MATRIX_MODEL] = rl.get_shader_location(shader, "matModel")
    shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")

    # Ambient light level
    ambient_loc = rl.get_shader_location(shader, "ambient")
    ambient = rl.ffi.new("float[4]", [0.2, 0.2, 0.2, 1.0])
    rl.set_shader_value(shader, ambient_loc, ambient, rl.SHADER_UNIFORM_VEC4)

    fog_density = 0.15
    fog_density_loc = rl.get_shader_location(shader, "fogDensity")
    rl.set_shader_value(shader, fog_density_loc, rl.ffi.new("float *", fog_density), rl.SHADER_UNIFORM_FLOAT)

    # NOTE: All models share the same shader
    model_a.materials[0].shader = shader
    model_b.materials[0].shader = shader
    model_c.materials[0].shader = shader

    # Using just 1 point light
    create_light(LIGHT_POINT, rl.Vector3(0, 2, 6), rl.Vector3(0, 0, 0), rl.WHITE, shader)

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():     # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)

        if rl.is_key_down(rl.KEY_UP):
            fog_density += 0.001
            if fog_density > 1.0:
                fog_density = 1.0

        if rl.is_key_down(rl.KEY_DOWN):
            fog_density -= 0.001
            if fog_density < 0.0:
                fog_density = 0.0

        rl.set_shader_value(shader, fog_density_loc, rl.ffi.new("float *", fog_density), rl.SHADER_UNIFORM_FLOAT)

        # Rotate the torus
        model_a.transform = rl.matrix_multiply(model_a.transform, rl.matrix_rotate_x(-0.025))
        model_a.transform = rl.matrix_multiply(model_a.transform, rl.matrix_rotate_z(0.012))

        # Update the light shader with the camera view position
        camera_pos = rl.ffi.new("float[3]", [camera.position.x, camera.position.y, camera.position.z])
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], camera_pos, rl.SHADER_UNIFORM_VEC3)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.GRAY)

        rl.begin_mode_3d(camera)

        # Draw the three models
        rl.draw_model(model_a, rl.Vector3(0, 0, 0), 1.0, rl.WHITE)
        rl.draw_model(model_b, rl.Vector3(-2.6, 0, 0), 1.0, rl.WHITE)
        rl.draw_model(model_c, rl.Vector3(2.6, 0, 0), 1.0, rl.WHITE)

        for i in range(-20, 20, 2):
            rl.draw_model(model_a, rl.Vector3(float(i), 0, 2), 1.0, rl.WHITE)

        rl.end_mode_3d()

        rl.draw_text(f"Use KEY_UP/KEY_DOWN to change fog density [{fog_density:.2f}]", 10, 10, 20, rl.RAYWHITE)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model_a)        # Unload the model A
    rl.unload_model(model_b)        # Unload the model B
    rl.unload_model(model_c)        # Unload the model C
    rl.unload_texture(texture)      # Unload the texture
    rl.unload_shader(shader)        # Unload shader

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()