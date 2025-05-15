"""raylib [shaders] example - basic lighting
Example complexity rating: [★★★★] 4/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3).
Example originally created with raylib 3.0, last time updated with raylib 4.2
Example contributed by Chris Camacho (@chriscamacho) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Chris Camacho (@chriscamacho) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Import our lights helper
from rlights import create_light, update_light_values, MAX_LIGHTS, LIGHT_POINT

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
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - basic lighting")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(2.0, 4.0, 6.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.5, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load basic lighting shader
    shader = rl.load_shader(
        str(THIS_DIR/"resources/shaders/glsl{}/lighting.vs".format(GLSL_VERSION)),
        str(THIS_DIR/"resources/shaders/glsl{}/lighting.fs".format(GLSL_VERSION))
    )

    # Get some required shader locations
    shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")
    # NOTE: "matModel" location name is automatically assigned on shader loading, 
    # no need to get the location again if using that uniform name
    #shader.locs[rl.SHADER_LOC_MATRIX_MODEL] = rl.get_shader_location(shader, "matModel")
    
    # Ambient light level (some basic lighting)
    ambient_loc = rl.get_shader_location(shader, "ambient")
    values = rl.ffi.new("float[4]", [0.1, 0.1, 0.1, 1.0])
    rl.set_shader_value(shader, ambient_loc, values, rl.SHADER_UNIFORM_VEC4)    # Create lights
    lights = [None] * MAX_LIGHTS
    lights[0] = create_light(LIGHT_POINT, rl.Vector3(-2, 1, -2), rl.Vector3(0, 0, 0), rl.YELLOW, shader)
    lights[1] = create_light(LIGHT_POINT, rl.Vector3(2, 1, 2), rl.Vector3(0, 0, 0), rl.RED, shader)
    lights[2] = create_light(LIGHT_POINT, rl.Vector3(-2, 1, 2), rl.Vector3(0, 0, 0), rl.GREEN, shader)
    lights[3] = create_light(LIGHT_POINT, rl.Vector3(2, 1, -2), rl.Vector3(0, 0, 0), rl.BLUE, shader)

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():     # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.ffi.addressof(camera), rl.CAMERA_ORBITAL)

        # Update the shader with the camera view vector (points towards { 0.0f, 0.0f, 0.0f })
        camera_pos = rl.ffi.new("float[3]", [camera.position.x, camera.position.y, camera.position.z])
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], camera_pos, rl.SHADER_UNIFORM_VEC3)
        
        # Check key inputs to enable/disable lights
        if rl.is_key_pressed(rl.KEY_Y): 
            lights[0].enabled = not lights[0].enabled
        
        if rl.is_key_pressed(rl.KEY_R): 
            lights[1].enabled = not lights[1].enabled
        
        if rl.is_key_pressed(rl.KEY_G): 
            lights[2].enabled = not lights[2].enabled
        
        if rl.is_key_pressed(rl.KEY_B): 
            lights[3].enabled = not lights[3].enabled
        
        # Update light values (actually, only enable/disable them)
        for i in range(MAX_LIGHTS):
            update_light_values(shader, lights[i])
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.begin_shader_mode(shader)

        rl.draw_plane(rl.Vector3(0, 0, 0), rl.Vector2(10.0, 10.0), rl.WHITE)
        rl.draw_cube(rl.Vector3(0, 0, 0), 2.0, 4.0, 2.0, rl.WHITE)

        rl.end_shader_mode()

        # Draw spheres to show where the lights are
        for i in range(MAX_LIGHTS):
            if lights[i].enabled:
                rl.draw_sphere_ex(lights[i].position, 0.2, 8, 8, lights[i].color)
            else:
                rl.draw_sphere_wires(lights[i].position, 0.2, 8, 8, 
                                     rl.color_alpha(lights[i].color, 0.3))

        rl.draw_grid(10, 1.0)

        rl.end_mode_3d()

        rl.draw_fps(10, 10)

        rl.draw_text("Use keys [Y][R][G][B] to toggle lights", 10, 40, 20, rl.DARKGRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(shader)   # Unload shader

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()