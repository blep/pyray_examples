"""raylib [models] example - Load models vox (MagicaVoxel)
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 4.0, last time updated with raylib 4.0
Example contributed by Johann Nadalutti (@procfxgen) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Johann Nadalutti (@procfxgen) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import os
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Define constants
MAX_VOX_FILES = 4
MAX_LIGHTS = 4

# Define platform for shader version
GLSL_VERSION = 330
# GLSL_VERSION = 100 # No shaders available for GLSL_VERSION 1.0; original code decide based on PLATFORM_DESKTOP

# Light type enumeration
LIGHT_DIRECTIONAL = 0
LIGHT_POINT = 1

# Light data class (replacement for C struct)
class Light:
    def __init__(self):
        self.type = 0
        self.enabled = False
        self.position = rl.Vector3(0, 0, 0)
        self.target = rl.Vector3(0, 0, 0)
        self.color = rl.BLACK
        # Shader locations/values
        self.enabled_loc = -1
        self.type_loc = -1
        self.position_loc = -1
        self.target_loc = -1
        self.color_loc = -1

# Function to create a light
def create_light(type, position, target, color, shader):
    light = Light()
    light.type = type
    light.enabled = True
    light.position = position
    light.target = target
    light.color = color
    
    # Get shader locations for light properties
    light.enabled_loc = rl.get_shader_location(shader, f"lights[{next_light}].enabled")
    light.type_loc = rl.get_shader_location(shader, f"lights[{next_light}].type")
    light.position_loc = rl.get_shader_location(shader, f"lights[{next_light}].position")
    light.target_loc = rl.get_shader_location(shader, f"lights[{next_light}].target")
    light.color_loc = rl.get_shader_location(shader, f"lights[{next_light}].color")
    
    # Set shader values for this light
    update_light_values(shader, light)
    
    return light

# Function to update light values
def update_light_values(shader, light):
    # Send to shader light enabled state and type
    rl.set_shader_value(shader, light.enabled_loc, rl.ffi.new("int*", int(light.enabled)), rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(shader, light.type_loc, rl.ffi.new("int*", light.type), rl.SHADER_UNIFORM_INT)
    
    # Send to shader light position values
    rl.set_shader_value(shader, light.position_loc, rl.ffi.addressof(light.position), rl.SHADER_UNIFORM_VEC3)
    
    # Send to shader light target position values
    rl.set_shader_value(shader, light.target_loc, rl.ffi.addressof(light.target), rl.SHADER_UNIFORM_VEC3)
    
    # Send to shader light color values
    # Assuming light.color is a tuple (r, g, b, a)
    normalized_color = [light.color[0]/255.0, light.color[1]/255.0, light.color[2]/255.0, light.color[3]/255.0]
    rl.set_shader_value(shader, light.color_loc, rl.ffi.new("float[]", normalized_color), rl.SHADER_UNIFORM_VEC4)

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    vox_file_names = [
        str(THIS_DIR/"resources/models/vox/chr_knight.vox"),
        str(THIS_DIR/"resources/models/vox/chr_sword.vox"),
        str(THIS_DIR/"resources/models/vox/monu9.vox"),
        str(THIS_DIR/"resources/models/vox/fez.vox")
    ]

    rl.init_window(screen_width, screen_height, "raylib [models] example - magicavoxel loading")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(10.0, 10.0, 10.0)  # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)       # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 45.0                              # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE       # Camera projection type

    #--------------------------------------------------------------------------------------
    # Load MagicaVoxel files
    models = [None] * MAX_VOX_FILES

    for i in range(MAX_VOX_FILES):
        # Load VOX file and measure time
        t0 = rl.get_time() * 1000.0
        models[i] = rl.load_model(vox_file_names[i])
        t1 = rl.get_time() * 1000.0

        rl.trace_log(rl.LOG_WARNING, f"[{vox_file_names[i]}] File loaded in {t1 - t0:.3f} ms")

        # Compute model translation matrix to center model on draw position (0, 0 , 0)
        bb = rl.get_model_bounding_box(models[i])
        center = rl.Vector3(0, 0, 0)
        center.x = bb.min.x + (((bb.max.x - bb.min.x) / 2))
        center.z = bb.min.z + (((bb.max.z - bb.min.z) / 2))

        mat_translate = rl.matrix_translate(-center.x, 0, -center.z)
        models[i].transform = mat_translate

    current_model = 0

    #--------------------------------------------------------------------------------------
    # Load voxel shader
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/voxel_lighting.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/voxel_lighting.fs")
    )

    # Get some required shader locations
    shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")
    # NOTE: "matModel" location name is automatically assigned on shader loading, 
    # no need to get the location again if using that uniform name

    # Ambient light level (some basic lighting)
    ambient_loc = rl.get_shader_location(shader, "ambient")
    rl.set_shader_value(shader, ambient_loc, rl.ffi.new("float[]", [0.1, 0.1, 0.1, 1.0]), rl.SHADER_UNIFORM_VEC4)

    # Assign our lighting shader to model
    for i in range(MAX_VOX_FILES):
        m = models[i]
        for j in range(m.materialCount):
            m.materials[j].shader = shader

    # Create lights
    lights = [None] * MAX_LIGHTS
    next_light = 0  # Used by create_light function
    
    lights[0] = create_light(LIGHT_POINT, rl.Vector3(-20, 20, -20), rl.Vector3(0, 0, 0), rl.GRAY, shader)
    next_light += 1
    lights[1] = create_light(LIGHT_POINT, rl.Vector3(20, -20, 20), rl.Vector3(0, 0, 0), rl.GRAY, shader)
    next_light += 1
    lights[2] = create_light(LIGHT_POINT, rl.Vector3(-20, 20, 20), rl.Vector3(0, 0, 0), rl.GRAY, shader)
    next_light += 1
    lights[3] = create_light(LIGHT_POINT, rl.Vector3(20, -20, -20), rl.Vector3(0, 0, 0), rl.GRAY, shader)

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second

    #--------------------------------------------------------------------------------------
    model_pos = rl.Vector3(0, 0, 0)
    camera_rot = rl.Vector3(0, 0, 0)

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_MIDDLE):
            mouse_delta = rl.get_mouse_delta()
            camera_rot.x = mouse_delta.x * 0.05
            camera_rot.y = mouse_delta.y * 0.05
        else:
            camera_rot.x = 0
            camera_rot.y = 0

        # Create the camera movement vector
        camera_movement = rl.Vector3(
            (rl.is_key_down(rl.KEY_W) or rl.is_key_down(rl.KEY_UP)) * 0.1 -
            (rl.is_key_down(rl.KEY_S) or rl.is_key_down(rl.KEY_DOWN)) * 0.1,
            
            (rl.is_key_down(rl.KEY_D) or rl.is_key_down(rl.KEY_RIGHT)) * 0.1 -
            (rl.is_key_down(rl.KEY_A) or rl.is_key_down(rl.KEY_LEFT)) * 0.1,
            
            0.0
        )
        
        # Update camera with pro function
        rl.update_camera_pro(camera, camera_movement, camera_rot, rl.get_mouse_wheel_move() * -2.0)

        # Cycle between models on mouse click
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            current_model = (current_model + 1) % MAX_VOX_FILES

        # Update the shader with the camera view vector (points towards { 0.0f, 0.0f, 0.0f })
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], rl.ffi.addressof(camera.position), rl.SHADER_UNIFORM_VEC3)

        # Update light values (actually, only enable/disable them)
        for i in range(MAX_LIGHTS):
            update_light_values(shader, lights[i])

        #----------------------------------------------------------------------------------
        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        # Draw 3D model
        rl.begin_mode_3d(camera)

        rl.draw_model(models[current_model], model_pos, 1.0, rl.WHITE)
        rl.draw_grid(10, 1.0)

        # Draw spheres to show where the lights are
        for i in range(MAX_LIGHTS):
            if lights[i].enabled:
                rl.draw_sphere_ex(lights[i].position, 0.2, 8, 8, lights[i].color)
            else:
                rl.draw_sphere_wires(lights[i].position, 0.2, 8, 8, rl.fade(lights[i].color, 0.3))

        rl.end_mode_3d()

        # Display info
        rl.draw_rectangle(10, 400, 340, 60, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(10, 400, 340, 60, rl.fade(rl.DARKBLUE, 0.5))
        rl.draw_text("MOUSE LEFT BUTTON to CYCLE VOX MODELS", 40, 410, 10, rl.BLUE)
        rl.draw_text("MOUSE MIDDLE BUTTON to ZOOM OR ROTATE CAMERA", 40, 420, 10, rl.BLUE)
        rl.draw_text("UP-DOWN-LEFT-RIGHT KEYS to MOVE CAMERA", 40, 430, 10, rl.BLUE)
        rl.draw_text(f"File: {os.path.basename(vox_file_names[current_model])}", 10, 10, 20, rl.GRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    # Unload models data (GPU VRAM)
    for i in range(MAX_VOX_FILES):
        rl.unload_model(models[i])

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
