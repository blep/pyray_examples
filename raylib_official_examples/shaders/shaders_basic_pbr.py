"""raylib [shaders] example - Basic PBR
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 5.0, last time updated with raylib 5.1-dev
Example contributed by Afan OLOVCIC (@_DevDad) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Afan OLOVCIC (@_DevDad)
Model: "Old Rusty Car" (https://skfb.ly/LxRy) by Renafox, 
licensed under Creative Commons Attribution-NonCommercial 
(http://creativecommons.org/licenses/by-nc/4.0/)

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

# Max dynamic lights supported by shader
MAX_LIGHTS = 4

# Light types
LIGHT_DIRECTIONAL = 0
LIGHT_POINT = 1
LIGHT_SPOT = 2

# Global variable to keep track of the number of lights
light_count = 0

class Light:
    def __init__(self):
        self.type = 0
        self.enabled = 1
        self.position = rl.Vector3(0, 0, 0)
        self.target = rl.Vector3(0, 0, 0)
        self.color = [0, 0, 0, 0]  # float[4]
        self.intensity = 0.0
        
        # Shader locations
        self.enabled_loc = 0
        self.type_loc = 0
        self.position_loc = 0
        self.target_loc = 0
        self.color_loc = 0
        self.intensity_loc = 0

def create_light(light_type, position, target, color, intensity, shader):
    """Create a light and get shader locations"""
    global light_count
    
    light = Light()
    
    if light_count < MAX_LIGHTS:
        light.enabled = 1
        light.type = light_type
        light.position = position
        light.target = target
        light.color = [color[0]/255.0, color[1]/255.0, color[2]/255.0, color[3]/255.0]
        light.intensity = intensity
        
        # NOTE: Shader parameters names for lights must match the requested ones
        light.enabled_loc = rl.get_shader_location(shader, f"lights[{light_count}].enabled")
        light.type_loc = rl.get_shader_location(shader, f"lights[{light_count}].type")
        light.position_loc = rl.get_shader_location(shader, f"lights[{light_count}].position")
        light.target_loc = rl.get_shader_location(shader, f"lights[{light_count}].target")
        light.color_loc = rl.get_shader_location(shader, f"lights[{light_count}].color")
        light.intensity_loc = rl.get_shader_location(shader, f"lights[{light_count}].intensity")
        
        update_light(shader, light)
        
        light_count += 1
    
    return light

def update_light(shader, light):
    """Send light properties to shader"""
    # Send to shader light enabled state and type
    rl.set_shader_value(shader, light.enabled_loc, rl.ffi.new("int *", light.enabled), rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(shader, light.type_loc, rl.ffi.new("int *", light.type), rl.SHADER_UNIFORM_INT)
    
    # Send to shader light position values
    position = rl.ffi.new("float[3]", [light.position.x, light.position.y, light.position.z])
    rl.set_shader_value(shader, light.position_loc, position, rl.SHADER_UNIFORM_VEC3)
    
    # Send to shader light target position values
    target = rl.ffi.new("float[3]", [light.target.x, light.target.y, light.target.z])
    rl.set_shader_value(shader, light.target_loc, target, rl.SHADER_UNIFORM_VEC3)
    
    # Send to shader light color and intensity values
    color = rl.ffi.new("float[4]", light.color)
    rl.set_shader_value(shader, light.color_loc, color, rl.SHADER_UNIFORM_VEC4)
    rl.set_shader_value(shader, light.intensity_loc, rl.ffi.new("float *", light.intensity), rl.SHADER_UNIFORM_FLOAT)

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - basic pbr")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(2.0, 2.0, 6.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.5, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load PBR shader and setup all required locations
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/pbr.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/pbr.fs")
    )
    
    shader.locs[rl.SHADER_LOC_MAP_ALBEDO] = rl.get_shader_location(shader, "albedoMap")
    # WARNING: Metalness, roughness, and ambient occlusion are all packed into a MRA texture
    # They are passed as to the SHADER_LOC_MAP_METALNESS location for convenience,
    # shader already takes care of it accordingly
    shader.locs[rl.SHADER_LOC_MAP_METALNESS] = rl.get_shader_location(shader, "mraMap")
    shader.locs[rl.SHADER_LOC_MAP_NORMAL] = rl.get_shader_location(shader, "normalMap")
    # WARNING: Similar to the MRA map, the emissive map packs different information 
    # into a single texture: it stores height and emission data
    # It is binded to SHADER_LOC_MAP_EMISSION location an properly processed on shader
    shader.locs[rl.SHADER_LOC_MAP_EMISSION] = rl.get_shader_location(shader, "emissiveMap")
    shader.locs[rl.SHADER_LOC_COLOR_DIFFUSE] = rl.get_shader_location(shader, "albedoColor")

    # Setup additional required shader locations, including lights data
    shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shader, "viewPos")
    light_count_loc = rl.get_shader_location(shader, "numOfLights")
    max_light_count = MAX_LIGHTS
    rl.set_shader_value(shader, light_count_loc, rl.ffi.new("int *", max_light_count), rl.SHADER_UNIFORM_INT)

    # Setup ambient color and intensity parameters
    ambient_intensity = 0.02
    ambient_color = rl.Color(26, 32, 135, 255)
    ambient_color_normalized = rl.ffi.new("float[3]", [ambient_color.r/255.0, ambient_color.g/255.0, ambient_color.b/255.0])
    rl.set_shader_value(shader, rl.get_shader_location(shader, "ambientColor"), ambient_color_normalized, rl.SHADER_UNIFORM_VEC3)
    rl.set_shader_value(shader, rl.get_shader_location(shader, "ambient"), rl.ffi.new("float *", ambient_intensity), rl.SHADER_UNIFORM_FLOAT)

    # Get location for shader parameters that can be modified in real time
    emissive_intensity_loc = rl.get_shader_location(shader, "emissivePower")
    emissive_color_loc = rl.get_shader_location(shader, "emissiveColor")
    texture_tiling_loc = rl.get_shader_location(shader, "tiling")

    # Load old car model using PBR maps and shader
    # WARNING: We know this model consists of a single model.meshes[0] and
    # that model.materials[0] is by default assigned to that mesh
    car = rl.load_model(str(THIS_DIR/"resources/models/old_car_new.glb"))

    # Assign already setup PBR shader to model.materials[0], used by models.meshes[0]
    car.materials[0].shader = shader

    # Setup materials[0].maps default parameters
    car.materials[0].maps[rl.MATERIAL_MAP_ALBEDO].color = rl.WHITE
    car.materials[0].maps[rl.MATERIAL_MAP_METALNESS].value = 0.0
    car.materials[0].maps[rl.MATERIAL_MAP_ROUGHNESS].value = 0.0
    car.materials[0].maps[rl.MATERIAL_MAP_OCCLUSION].value = 1.0
    car.materials[0].maps[rl.MATERIAL_MAP_EMISSION].color = rl.Color(255, 162, 0, 255)

    # Setup materials[0].maps default textures
    car.materials[0].maps[rl.MATERIAL_MAP_ALBEDO].texture = rl.load_texture(str(THIS_DIR/"resources/old_car_d.png"))
    car.materials[0].maps[rl.MATERIAL_MAP_METALNESS].texture = rl.load_texture(str(THIS_DIR/"resources/old_car_mra.png"))
    car.materials[0].maps[rl.MATERIAL_MAP_NORMAL].texture = rl.load_texture(str(THIS_DIR/"resources/old_car_n.png"))
    car.materials[0].maps[rl.MATERIAL_MAP_EMISSION].texture = rl.load_texture(str(THIS_DIR/"resources/old_car_e.png"))
    
    # Load floor model mesh and assign material parameters
    floor = rl.load_model(str(THIS_DIR/"resources/models/plane.glb"))

    # Assign material shader for our floor model, same PBR shader 
    floor.materials[0].shader = shader
    
    floor.materials[0].maps[rl.MATERIAL_MAP_ALBEDO].color = rl.WHITE
    floor.materials[0].maps[rl.MATERIAL_MAP_METALNESS].value = 0.0
    floor.materials[0].maps[rl.MATERIAL_MAP_ROUGHNESS].value = 0.0
    floor.materials[0].maps[rl.MATERIAL_MAP_OCCLUSION].value = 1.0
    floor.materials[0].maps[rl.MATERIAL_MAP_EMISSION].color = rl.BLACK

    floor.materials[0].maps[rl.MATERIAL_MAP_ALBEDO].texture = rl.load_texture(str(THIS_DIR/"resources/road_a.png"))
    floor.materials[0].maps[rl.MATERIAL_MAP_METALNESS].texture = rl.load_texture(str(THIS_DIR/"resources/road_mra.png"))
    floor.materials[0].maps[rl.MATERIAL_MAP_NORMAL].texture = rl.load_texture(str(THIS_DIR/"resources/road_n.png"))

    # Models texture tiling parameter can be stored in the Material struct if required
    car_texture_tiling = rl.ffi.new("float[2]", [0.5, 0.5])
    floor_texture_tiling = rl.ffi.new("float[2]", [0.5, 0.5])

    # Create some lights
    lights = [None] * MAX_LIGHTS
    lights[0] = create_light(LIGHT_POINT, rl.Vector3(-1.0, 1.0, -2.0), rl.Vector3(0.0, 0.0, 0.0), rl.YELLOW, 4.0, shader)
    lights[1] = create_light(LIGHT_POINT, rl.Vector3(2.0, 1.0, 1.0), rl.Vector3(0.0, 0.0, 0.0), rl.GREEN, 3.3, shader)
    lights[2] = create_light(LIGHT_POINT, rl.Vector3(-2.0, 1.0, 1.0), rl.Vector3(0.0, 0.0, 0.0), rl.RED, 8.3, shader)
    lights[3] = create_light(LIGHT_POINT, rl.Vector3(1.0, 1.0, -2.0), rl.Vector3(0.0, 0.0, 0.0), rl.BLUE, 2.0, shader)

    # Setup material texture maps usage in shader
    # NOTE: By default, the texture maps are always used
    usage = 1
    rl.set_shader_value(shader, rl.get_shader_location(shader, "useTexAlbedo"), rl.ffi.new("int *", usage), rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(shader, rl.get_shader_location(shader, "useTexNormal"), rl.ffi.new("int *", usage), rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(shader, rl.get_shader_location(shader, "useTexMRA"), rl.ffi.new("int *", usage), rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(shader, rl.get_shader_location(shader, "useTexEmissive"), rl.ffi.new("int *", usage), rl.SHADER_UNIFORM_INT)
    
    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #---------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.ffi.addressof(camera), rl.CAMERA_ORBITAL)

        # Update the shader with the camera view vector (points towards { 0.0f, 0.0f, 0.0f })
        camera_pos = rl.ffi.new("float[3]", [camera.position.x, camera.position.y, camera.position.z])
        rl.set_shader_value(shader, shader.locs[rl.SHADER_LOC_VECTOR_VIEW], camera_pos, rl.SHADER_UNIFORM_VEC3)

        # Check key inputs to enable/disable lights
        if rl.is_key_pressed(rl.KEY_ONE): 
            lights[2].enabled = not lights[2].enabled
            
        if rl.is_key_pressed(rl.KEY_TWO): 
            lights[1].enabled = not lights[1].enabled
            
        if rl.is_key_pressed(rl.KEY_THREE): 
            lights[3].enabled = not lights[3].enabled
            
        if rl.is_key_pressed(rl.KEY_FOUR): 
            lights[0].enabled = not lights[0].enabled

        # Update light values on shader (actually, only enable/disable them)
        for i in range(MAX_LIGHTS):
            update_light(shader, lights[i])
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.BLACK)
        
        rl.begin_mode_3d(camera)
            
        # Set floor model texture tiling and emissive color parameters on shader
        rl.set_shader_value(shader, texture_tiling_loc, floor_texture_tiling, rl.SHADER_UNIFORM_VEC2)
        floor_emissive_color = rl.color_normalize(floor.materials[0].maps[rl.MATERIAL_MAP_EMISSION].color)
        rl.set_shader_value(shader, emissive_color_loc, rl.ffi.addressof(floor_emissive_color), rl.SHADER_UNIFORM_VEC4)

        rl.draw_model(floor, rl.Vector3(0.0, 0.0, 0.0), 5.0, rl.WHITE)   # Draw floor model

        # Set old car model texture tiling, emissive color and emissive intensity parameters on shader
        rl.set_shader_value(shader, texture_tiling_loc, car_texture_tiling, rl.SHADER_UNIFORM_VEC2)
        car_emissive_color = rl.color_normalize(car.materials[0].maps[rl.MATERIAL_MAP_EMISSION].color)
        rl.set_shader_value(shader, emissive_color_loc, rl.ffi.addressof(car_emissive_color), rl.SHADER_UNIFORM_VEC4)
        emissive_intensity = 0.01
        rl.set_shader_value(shader, emissive_intensity_loc, rl.ffi.new("float *", emissive_intensity), rl.SHADER_UNIFORM_FLOAT)

        rl.draw_model(car, rl.Vector3(0.0, 0.0, 0.0), 0.25, rl.WHITE)   # Draw car model

        # Draw spheres to show the lights positions
        for i in range(MAX_LIGHTS):
            light_color = rl.Color(
                int(lights[i].color[0]*255),
                int(lights[i].color[1]*255),
                int(lights[i].color[2]*255),
                int(lights[i].color[3]*255)
            )

            if lights[i].enabled:
                rl.draw_sphere_ex(lights[i].position, 0.2, 8, 8, light_color)
            else:
                rl.draw_sphere_wires(lights[i].position, 0.2, 8, 8, rl.color_alpha(light_color, 0.3))
            
        rl.end_mode_3d()
        
        rl.draw_text("Toggle lights: [1][2][3][4]", 10, 40, 20, rl.LIGHTGRAY)

        rl.draw_text("(c) Old Rusty Car model by Renafox (https://skfb.ly/LxRy)", screen_width - 320, screen_height - 20, 10, rl.LIGHTGRAY)
        
        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    # Unbind (disconnect) shader from car.material[0] 
    # to avoid UnloadMaterial() trying to unload it automatically
    car.materials[0].shader.id = 0
    rl.unload_material(car.materials[0])
    car.materials[0].maps = None
    rl.unload_model(car)
    
    floor.materials[0].shader.id = 0
    rl.unload_material(floor.materials[0])
    floor.materials[0].maps = None
    rl.unload_model(floor)
    
    rl.unload_shader(shader)       # Unload Shader
    
    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()