"""raylib [shaders] example - Shadowmap
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 5.0, last time updated with raylib 5.0
Example contributed by TheManTheMythTheGameDev (@TheManTheMythTheGameDev) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 TheManTheMythTheGameDev (@TheManTheMythTheGameDev)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 120
else:
    GLSL_VERSION = 330

SHADOWMAP_RESOLUTION = 1024

def load_shadowmap_render_texture(width, height):
    target = rl.RenderTexture()

    target.id = rl.rl_load_framebuffer()  # Load an empty framebuffer
    target.texture.width = width
    target.texture.height = height

    if target.id > 0:
        rl.rl_enable_framebuffer(target.id)

        # Create depth texture
        # We don't need a color texture for the shadowmap
        target.depth.id = rl.rl_load_texture_depth(width, height, False)
        target.depth.width = width
        target.depth.height = height
        target.depth.format = 19      # DEPTH_COMPONENT_24BIT?
        target.depth.mipmaps = 1

        # Attach depth texture to FBO
        rl.rl_framebuffer_attach(target.id, target.depth.id, rl.RL_ATTACHMENT_DEPTH, rl.RL_ATTACHMENT_TEXTURE2D, 0)

        # Check if fbo is complete with attachments (valid)
        if rl.rl_framebuffer_complete(target.id):
            rl.trace_log(rl.LOG_INFO, f"FBO: [ID {target.id}] Framebuffer object created successfully")

        rl.rl_disable_framebuffer()
    else:
        rl.trace_log(rl.LOG_WARNING, "FBO: Framebuffer object can not be created")

    return target

# Unload shadowmap render texture from GPU memory (VRAM)
def unload_shadowmap_render_texture(target):
    if target.id > 0:
        # NOTE: Depth texture/renderbuffer is automatically
        # queried and deleted before deleting framebuffer
        rl.rl_unload_framebuffer(target.id)

def draw_scene(cube, robot):
    rl.draw_model_ex(cube, rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(0.0, 1.0, 0.0), 0.0, rl.Vector3(10.0, 1.0, 10.0), rl.BLUE)
    rl.draw_model_ex(cube, rl.Vector3(1.5, 1.0, -1.5), rl.Vector3(0.0, 1.0, 0.0), 0.0, rl.Vector3(1.0, 1.0, 1.0), rl.WHITE)
    rl.draw_model_ex(robot, rl.Vector3(0.0, 0.5, 0.0), rl.Vector3(0.0, 1.0, 0.0), 0.0, rl.Vector3(1.0, 1.0, 1.0), rl.RED)

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)
    # Shadows are a HUGE topic, and this example shows an extremely simple implementation of the shadowmapping algorithm,
    # which is the industry standard for shadows. This algorithm can be extended in a ridiculous number of ways to improve
    # realism and also adapt it for different scenes. This is pretty much the simplest possible implementation.
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - shadowmap")

    cam = rl.Camera3D()
    cam.position = rl.Vector3(10.0, 10.0, 10.0)
    cam.target = rl.Vector3(0.0, 0.0, 0.0)
    cam.projection = rl.CAMERA_PERSPECTIVE
    cam.up = rl.Vector3(0.0, 1.0, 0.0)
    cam.fovy = 45.0

    shadow_shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/shadowmap.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/shadowmap.fs")
    )
    shadow_shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(shadow_shader, "viewPos")
    light_dir = rl.vector3_normalize(rl.Vector3(0.35, -1.0, -0.35))
    light_color = rl.WHITE
    light_color_normalized = rl.color_normalize(light_color)
    light_dir_loc = rl.get_shader_location(shadow_shader, "lightDir")
    light_col_loc = rl.get_shader_location(shadow_shader, "lightColor")
    
    rl.set_shader_value(shadow_shader, light_dir_loc, rl.ffi.new("Vector3 *", [light_dir.x, light_dir.y, light_dir.z]), rl.SHADER_UNIFORM_VEC3)
    rl.set_shader_value(shadow_shader, light_col_loc, rl.ffi.new("Vector4 *", [light_color_normalized.x, light_color_normalized.y, light_color_normalized.z, light_color_normalized.w]), rl.SHADER_UNIFORM_VEC4)
    
    ambient_loc = rl.get_shader_location(shadow_shader, "ambient")
    ambient = rl.ffi.new("float[4]", [0.1, 0.1, 0.1, 1.0])
    rl.set_shader_value(shadow_shader, ambient_loc, ambient, rl.SHADER_UNIFORM_VEC4)
    
    light_vp_loc = rl.get_shader_location(shadow_shader, "lightVP")
    shadow_map_loc = rl.get_shader_location(shadow_shader, "shadowMap")
    shadow_map_resolution_value = rl.ffi.new("int *", SHADOWMAP_RESOLUTION)
    rl.set_shader_value(shadow_shader, rl.get_shader_location(shadow_shader, "shadowMapResolution"), shadow_map_resolution_value, rl.SHADER_UNIFORM_INT)

    cube = rl.load_model_from_mesh(rl.gen_mesh_cube(1.0, 1.0, 1.0))
    cube.materials[0].shader = shadow_shader
    robot = rl.load_model(str(THIS_DIR/"resources/models/robot.glb"))
    
    for i in range(robot.materialCount):
        robot.materials[i].shader = shadow_shader
    
    anim_count = rl.ffi.new("int *", 0)
    robot_animations = rl.load_model_animations(str(THIS_DIR/"resources/models/robot.glb"), anim_count)

    shadow_map = load_shadowmap_render_texture(SHADOWMAP_RESOLUTION, SHADOWMAP_RESOLUTION)
    # For the shadowmapping algorithm, we will be rendering everything from the light's point of view
    light_cam = rl.Camera3D()
    light_cam.position = rl.vector3_scale(light_dir, -15.0)
    light_cam.target = rl.Vector3(0.0, 0.0, 0.0)
    # Use an orthographic projection for directional lights
    light_cam.projection = rl.CAMERA_ORTHOGRAPHIC
    light_cam.up = rl.Vector3(0.0, 1.0, 0.0)
    light_cam.fovy = 20.0

    rl.set_target_fps(60)
    #--------------------------------------------------------------------------------------
    fc = 0

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        dt = rl.get_frame_time()

        camera_pos = rl.ffi.new("Vector3 *", [cam.position.x, cam.position.y, cam.position.z])
        rl.set_shader_value(shadow_shader, shadow_shader.locs[rl.SHADER_LOC_VECTOR_VIEW], camera_pos, rl.SHADER_UNIFORM_VEC3)
        rl.update_camera(cam, rl.CAMERA_ORBITAL)

        fc += 1
        fc %= robot_animations[0].frameCount
        rl.update_model_animation(robot, robot_animations[0], fc)

        camera_speed = 0.05
        if rl.is_key_down(rl.KEY_LEFT):
            if light_dir.x < 0.6:
                light_dir.x += camera_speed * 60.0 * dt
        if rl.is_key_down(rl.KEY_RIGHT):
            if light_dir.x > -0.6:
                light_dir.x -= camera_speed * 60.0 * dt
        if rl.is_key_down(rl.KEY_UP):
            if light_dir.z < 0.6:
                light_dir.z += camera_speed * 60.0 * dt
        if rl.is_key_down(rl.KEY_DOWN):
            if light_dir.z > -0.6:
                light_dir.z -= camera_speed * 60.0 * dt
                
        light_dir = rl.vector3_normalize(light_dir)
        light_cam.position = rl.vector3_scale(light_dir, -15.0)
        rl.set_shader_value(shadow_shader, light_dir_loc, rl.ffi.new("Vector3 *", [light_dir.x, light_dir.y, light_dir.z]), rl.SHADER_UNIFORM_VEC3)

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        # First, render all objects into the shadowmap
        # The idea is, we record all the objects' depths (as rendered from the light source's point of view) in a buffer
        # Anything that is "visible" to the light is in light, anything that isn't is in shadow
        # We can later use the depth buffer when rendering everything from the player's point of view
        # to determine whether a given point is "visible" to the light

        # Record the light matrices for future use!
        rl.begin_texture_mode(shadow_map)
        rl.clear_background(rl.WHITE)
        rl.begin_mode_3d(light_cam)
        light_view = rl.rl_get_matrix_modelview()
        light_proj = rl.rl_get_matrix_projection()
        draw_scene(cube, robot)
        rl.end_mode_3d()
        rl.end_texture_mode()
        light_view_proj = rl.matrix_multiply(light_view, light_proj)

        rl.clear_background(rl.RAYWHITE)

        rl.set_shader_value_matrix(shadow_shader, light_vp_loc, light_view_proj)

        rl.rl_enable_shader(shadow_shader.id)
        slot = 10  # Can be anything 0 to 15, but 0 will probably be taken up
        rl.rl_active_texture_slot(10)
        rl.rl_enable_texture(shadow_map.depth.id)
        rl.rl_set_uniform(shadow_map_loc, rl.ffi.new("int *", slot), rl.SHADER_UNIFORM_INT, 1)

        rl.begin_mode_3d(cam)

        # Draw the same exact things as we drew in the shadowmap!
        draw_scene(cube, robot)
        
        rl.end_mode_3d()

        rl.draw_text("Shadows in raylib using the shadowmapping algorithm!", screen_width - 320, screen_height - 20, 10, rl.GRAY)
        rl.draw_text("Use the arrow keys to rotate the light!", 10, 10, 30, rl.RED)

        rl.end_drawing()

        if rl.is_key_pressed(rl.KEY_F):
            rl.take_screenshot("shaders_shadowmap.png")
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------

    rl.unload_shader(shadow_shader)
    rl.unload_model(cube)
    rl.unload_model(robot)
    rl.unload_model_animations(robot_animations, anim_count[0])
    unload_shadowmap_render_texture(shadow_map)

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()