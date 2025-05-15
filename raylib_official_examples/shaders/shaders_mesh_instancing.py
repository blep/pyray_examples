"""raylib [shaders] example - Mesh instancing
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 3.7, last time updated with raylib 4.2
Example contributed by seanpringle (@seanpringle) and reviewed by Max (@moliad) and Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 seanpringle (@seanpringle), Max (@moliad) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import random
from pathlib import Path
from rlights import create_light

THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

MAX_INSTANCES = 10000

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - mesh instancing")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(-125.0, 125.0, -125.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)              # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)                  # Camera up vector (rotation towards target)
    camera.fovy = 45.0                                     # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE              # Camera projection type

    # Define mesh to be instanced
    cube = rl.gen_mesh_cube(1.0, 1.0, 1.0)

    # Allocate memory for transforms
    transforms_ptr = rl.rl_malloc(MAX_INSTANCES * rl.ffi.sizeof("Matrix"))
    # Create a python array view for easier manipulation
    transforms_array = rl.ffi.cast("Matrix *", transforms_ptr)

    # Translate and rotate cubes randomly
    for i in range(MAX_INSTANCES):
        translation = rl.matrix_translate(
            random.uniform(-50, 50),
            random.uniform(-50, 50),
            random.uniform(-50, 50)
        )
        axis = rl.vector3_normalize(rl.Vector3(
            random.uniform(0, 360),
            random.uniform(0, 360),
            random.uniform(0, 360)
        ))
        angle = random.uniform(0, 180) * rl.DEG2RAD
        rotation = rl.matrix_rotate(axis, angle)
        
        transforms_array[i] = rl.matrix_multiply(rotation, translation)

    # Load lighting shader
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/lighting_instancing.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/lighting.fs")
    )
    
    # Get shader locations
    shader.locs[rl.SHADER_LOC_MATRIX_MVP] = rl.get_shader_location(shader, "mvp")
    shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")

    # Set shader value: ambient light level
    ambient_loc = rl.get_shader_location(shader, "ambient")
    ambient_value = rl.ffi.new("float[4]", [0.2, 0.2, 0.2, 1.0])
    rl.set_shader_value(shader, ambient_loc, ambient_value, rl.SHADER_UNIFORM_VEC4)

    # Create one light
    create_light(rl.LIGHT_DIRECTIONAL, rl.Vector3(50.0, 50.0, 0.0), rl.Vector3(0, 0, 0), rl.WHITE, shader)

    # NOTE: We are assigning the instancing shader to material.shader
    # to be used on mesh drawing with DrawMeshInstanced()
    mat_instances = rl.load_material_default()
    mat_instances.shader = shader
    mat_instances.maps[rl.MATERIAL_MAP_DIFFUSE].color = rl.RED

    # Load default material (using raylib internal default shader) for non-instanced mesh drawing
    # WARNING: Default shader enables vertex color attribute BUT GenMeshCube() does not generate vertex colors, so,
    # when drawing the color attribute is disabled and a default color value is provided as input for the vertex attribute
    mat_default = rl.load_material_default()
    mat_default.maps[rl.MATERIAL_MAP_DIFFUSE].color = rl.BLUE

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.byref(camera), rl.CAMERA_ORBITAL)

        # Update the light shader with the camera view position
        camera_pos = rl.ffi.new("float[3]", [camera.position.x, camera.position.y, camera.position.z])
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], camera_pos, rl.SHADER_UNIFORM_VEC3)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        # Draw cube mesh with default material (BLUE)
        rl.draw_mesh(cube, mat_default, rl.matrix_translate(-10.0, 0.0, 0.0))

        # Draw meshes instanced using material containing instancing shader (RED + lighting),
        # transforms[] for the instances should be provided, they are dynamically
        # updated in GPU every frame, so we can animate the different mesh instances
        rl.draw_mesh_instanced(cube, mat_instances, transforms_ptr, MAX_INSTANCES)

        # Draw cube mesh with default material (BLUE)
        rl.draw_mesh(cube, mat_default, rl.matrix_translate(10.0, 0.0, 0.0))

        rl.end_mode_3d()

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.rl_free(transforms_ptr)    # Free transforms

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()