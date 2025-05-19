"""raylib [shaders] example - deferred rendering
Example complexity rating: [★★★★] 4/4
NOTE: This example requires raylib OpenGL 3.3 or OpenGL ES 3.0
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by Justin Andreas Lacoste (@27justin) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Justin Andreas Lacoste (@27justin)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import random
from dataclasses import dataclass
THIS_DIR = Path(__file__).resolve().parent

# Import the rlights module from local directory
from rlights import Light, create_light, update_light_values, LIGHT_POINT

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

MAX_CUBES = 30
MAX_LIGHTS = 4

# GBuffer data
@dataclass
class GBuffer:
    framebuffer: int = 0
    position_texture: int = 0
    normal_texture: int = 0
    albedo_spec_texture: int = 0
    depth_renderbuffer: int = 0

# Deferred mode passes
class DeferredMode:
    POSITION = 0
    NORMAL = 1
    ALBEDO = 2
    SHADING = 3

def main():
    # Initialization
    # -------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - deferred render")

    camera = rl.Camera3D()
    camera.position = rl.Vector3(5.0, 4.0, 5.0)    # Camera position
    camera.target = rl.Vector3(0.0, 1.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 60.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load plane model from a generated mesh
    model = rl.load_model_from_mesh(rl.gen_mesh_plane(10.0, 10.0, 3, 3))
    cube = rl.load_model_from_mesh(rl.gen_mesh_cube(2.0, 2.0, 2.0))

    # Load geometry buffer (G-buffer) shader and deferred shader
    gbuffer_shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/gbuffer.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/gbuffer.fs")
    )

    deferred_shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/deferred_shading.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/deferred_shading.fs")
    )
    deferred_shader.locs[rl.SHADER_LOC_VECTOR_VIEW] = rl.get_shader_location(deferred_shader, "viewPosition")

    # Initialize the G-buffer
    gbuffer = GBuffer()
    gbuffer.framebuffer = rl.rl_load_framebuffer()

    if not gbuffer.framebuffer:
        rl.tracelog(rl.LOG_WARNING, "Failed to create framebuffer")
        exit(1)
    
    rl.rl_enable_framebuffer(gbuffer.framebuffer)

    # NOTE: Vertex positions are stored in a texture for simplicity. A better approach would use a depth texture
    # (instead of a detph renderbuffer) to reconstruct world positions in the final render shader via clip-space position, 
    # depth, and the inverse view/projection matrices.

    # 16-bit precision ensures OpenGL ES 3 compatibility, though it may lack precision for real scenarios. 
    # But as mentioned above, the positions could be reconstructed instead of stored. If not targeting OpenGL ES
    # and you wish to maintain this approach, consider using `RL_PIXELFORMAT_UNCOMPRESSED_R32G32B32`.
    gbuffer.position_texture = rl.rl_load_texture(None, screen_width, screen_height, rl.RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16, 1)

    # Similarly, 16-bit precision is used for normals ensures OpenGL ES 3 compatibility.
    # This is generally sufficient, but a 16-bit fixed-point format offer a better uniform precision in all orientations.
    gbuffer.normal_texture = rl.rl_load_texture(None, screen_width, screen_height, rl.RL_PIXELFORMAT_UNCOMPRESSED_R16G16B16, 1)

    # Albedo (diffuse color) and specular strength can be combined into one texture.
    # The color in RGB, and the specular strength in the alpha channel.
    gbuffer.albedo_spec_texture = rl.rl_load_texture(None, screen_width, screen_height, rl.RL_PIXELFORMAT_UNCOMPRESSED_R8G8B8A8, 1)

    # Activate the draw buffers for our framebuffer
    rl.rl_active_draw_buffers(3)

    # Now we attach our textures to the framebuffer.
    rl.rl_framebuffer_attach(gbuffer.framebuffer, gbuffer.position_texture, rl.RL_ATTACHMENT_COLOR_CHANNEL0, rl.RL_ATTACHMENT_TEXTURE2D, 0)
    rl.rl_framebuffer_attach(gbuffer.framebuffer, gbuffer.normal_texture, rl.RL_ATTACHMENT_COLOR_CHANNEL1, rl.RL_ATTACHMENT_TEXTURE2D, 0)
    rl.rl_framebuffer_attach(gbuffer.framebuffer, gbuffer.albedo_spec_texture, rl.RL_ATTACHMENT_COLOR_CHANNEL2, rl.RL_ATTACHMENT_TEXTURE2D, 0)

    # Finally we attach the depth buffer.
    gbuffer.depth_renderbuffer = rl.rl_load_texture_depth(screen_width, screen_height, True)
    rl.rl_framebuffer_attach(gbuffer.framebuffer, gbuffer.depth_renderbuffer, rl.RL_ATTACHMENT_DEPTH, rl.RL_ATTACHMENT_RENDERBUFFER, 0)

    # Make sure our framebuffer is complete.
    # NOTE: rlFramebufferComplete() automatically unbinds the framebuffer, so we don't have
    # to rlDisableFramebuffer() here.
    if not rl.rl_framebuffer_complete(gbuffer.framebuffer):
        rl.tracelog(rl.LOG_WARNING, "Framebuffer is not complete")

    # Now we initialize the sampler2D uniform's in the deferred shader.
    # We do this by setting the uniform's values to the texture units that
    # we later bind our g-buffer textures to.
    rl.rl_enable_shader(deferred_shader.id)
    tex_unit_position = rl.ffi.new("int *", 0)
    tex_unit_normal = rl.ffi.new("int *", 1)
    tex_unit_albedo_spec = rl.ffi.new("int *", 2)
    rl.set_shader_value(deferred_shader, rl.rl_get_location_uniform(deferred_shader.id, "gPosition"), tex_unit_position, rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(deferred_shader, rl.rl_get_location_uniform(deferred_shader.id, "gNormal"), tex_unit_normal, rl.SHADER_UNIFORM_INT)
    rl.set_shader_value(deferred_shader, rl.rl_get_location_uniform(deferred_shader.id, "gAlbedoSpec"), tex_unit_albedo_spec, rl.SHADER_UNIFORM_INT)
    rl.rl_disable_shader()

    # Assign our lighting shader to model
    model.materials[0].shader = gbuffer_shader
    cube.materials[0].shader = gbuffer_shader

    # Create lights
    #--------------------------------------------------------------------------------------
    lights = [None] * MAX_LIGHTS
    lights[0] = create_light(LIGHT_POINT, rl.Vector3(-2, 1, -2), rl.Vector3(0, 0, 0), rl.YELLOW, deferred_shader)
    lights[1] = create_light(LIGHT_POINT, rl.Vector3(2, 1, 2), rl.Vector3(0, 0, 0), rl.RED, deferred_shader)
    lights[2] = create_light(LIGHT_POINT, rl.Vector3(-2, 1, 2), rl.Vector3(0, 0, 0), rl.GREEN, deferred_shader)
    lights[3] = create_light(LIGHT_POINT, rl.Vector3(2, 1, -2), rl.Vector3(0, 0, 0), rl.BLUE, deferred_shader)

    CUBE_SCALE = 0.25
    cube_positions = [rl.Vector3(0, 0, 0)] * MAX_CUBES
    cube_rotations = [0.0] * MAX_CUBES
    
    for i in range(MAX_CUBES):
        cube_positions[i] = rl.Vector3(
            random.randint(-5, 5),
            random.randint(0, 5),
            random.randint(-5, 5)
        )
        
        cube_rotations[i] = random.randint(0, 360)

    mode = DeferredMode.SHADING

    rl.rl_enable_depth_test()

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #---------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)

        # Update the shader with the camera view vector (points towards { 0.0f, 0.0f, 0.0f })
        camera_pos = rl.ffi.new("float[3]", [camera.position.x, camera.position.y, camera.position.z])
        rl.set_shader_value(deferred_shader, deferred_shader.locs[rl.SHADER_LOC_VECTOR_VIEW], camera_pos, rl.SHADER_UNIFORM_VEC3)
        
        # Check key inputs to enable/disable lights
        if rl.is_key_pressed(rl.KEY_Y):
            lights[0].enabled = not lights[0].enabled
        if rl.is_key_pressed(rl.KEY_R):
            lights[1].enabled = not lights[1].enabled
        if rl.is_key_pressed(rl.KEY_G):
            lights[2].enabled = not lights[2].enabled
        if rl.is_key_pressed(rl.KEY_B):
            lights[3].enabled = not lights[3].enabled

        # Check key inputs to switch between G-buffer textures
        if rl.is_key_pressed(rl.KEY_ONE):
            mode = DeferredMode.POSITION
        if rl.is_key_pressed(rl.KEY_TWO):
            mode = DeferredMode.NORMAL
        if rl.is_key_pressed(rl.KEY_THREE):
            mode = DeferredMode.ALBEDO
        if rl.is_key_pressed(rl.KEY_FOUR):
            mode = DeferredMode.SHADING

        # Update light values (actually, only enable/disable them)
        for i in range(MAX_LIGHTS):
            update_light_values(deferred_shader, lights[i])
        #----------------------------------------------------------------------------------

        # Draw
        # ---------------------------------------------------------------------------------
        rl.begin_drawing()

        # Draw to the geometry buffer by first activating it
        rl.rl_enable_framebuffer(gbuffer.framebuffer)
        rl.rl_clear_color(0, 0, 0, 0)
        rl.rl_clear_screen_buffers()  # Clear color and depth buffer
        
        rl.rl_disable_color_blend()
        rl.begin_mode_3d(camera)
        # NOTE: We have to use rlEnableShader here. `BeginShaderMode` or thus `rlSetShader`
        # will not work, as they won't immediately load the shader program.
        rl.rl_enable_shader(gbuffer_shader.id)
        # When drawing a model here, make sure that the material's shaders
        # are set to the gbuffer shader!
        rl.draw_model(model, rl.Vector3(0, 0, 0), 1.0, rl.WHITE)
        rl.draw_model(cube, rl.Vector3(0.0, 1.0, 0.0), 1.0, rl.WHITE)

        for i in range(MAX_CUBES):
            position = cube_positions[i]
            rl.draw_model_ex(cube, position, rl.Vector3(1, 1, 1), cube_rotations[i], rl.Vector3(CUBE_SCALE, CUBE_SCALE, CUBE_SCALE), rl.WHITE)

        rl.rl_disable_shader()
        rl.end_mode_3d()
        rl.rl_enable_color_blend()

        # Go back to the default framebuffer (0) and draw our deferred shading.
        rl.rl_disable_framebuffer()
        rl.rl_clear_screen_buffers() # Clear color & depth buffer

        if mode == DeferredMode.SHADING:
            rl.begin_mode_3d(camera)
            rl.rl_disable_color_blend()
            rl.rl_enable_shader(deferred_shader.id)
            # Bind our g-buffer textures
            # We are binding them to locations that we earlier set in sampler2D uniforms
            # `gPosition`, `gNormal`, and `gAlbedoSpec`
            rl.rl_active_texture_slot(tex_unit_position[0])
            rl.rl_enable_texture(gbuffer.position_texture)
            rl.rl_active_texture_slot(tex_unit_normal[0])
            rl.rl_enable_texture(gbuffer.normal_texture)
            rl.rl_active_texture_slot(tex_unit_albedo_spec[0])
            rl.rl_enable_texture(gbuffer.albedo_spec_texture)

            # Finally, we draw a fullscreen quad to our default framebuffer
            # This will now be shaded using our deferred shader
            rl.rl_load_draw_quad()
            rl.rl_disable_shader()
            rl.rl_enable_color_blend()
            rl.end_mode_3d()

            # As a last step, we now copy over the depth buffer from our g-buffer to the default framebuffer.
            rl.rl_bind_framebuffer(rl.RL_READ_FRAMEBUFFER, gbuffer.framebuffer)
            rl.rl_bind_framebuffer(rl.RL_DRAW_FRAMEBUFFER, 0)
            rl.rl_blit_framebuffer(0, 0, screen_width, screen_height, 0, 0, screen_width, screen_height, 0x00000100)  # GL_DEPTH_BUFFER_BIT
            rl.rl_disable_framebuffer()

            # Since our shader is now done and disabled, we can draw spheres
            # that represent light positions in default forward rendering
            rl.begin_mode_3d(camera)
            rl.rl_enable_shader(rl.rl_get_shader_id_default())
            for i in range(MAX_LIGHTS):
                if lights[i].enabled:
                    rl.draw_sphere_ex(lights[i].position, 0.2, 8, 8, lights[i].color)
                else:
                    rl.draw_sphere_wires(lights[i].position, 0.2, 8, 8, rl.color_alpha(lights[i].color, 0.3))
            rl.rl_disable_shader()
            rl.end_mode_3d()
            
            rl.draw_text("FINAL RESULT", 10, screen_height - 30, 20, rl.DARKGREEN)
        
        elif mode == DeferredMode.POSITION:
            texture = rl.Texture()
            texture.id = gbuffer.position_texture
            texture.width = screen_width
            texture.height = screen_height
            rl.draw_texture_rec(texture, rl.Rectangle(0, 0, screen_width, -screen_height), rl.Vector2(0, 0), rl.RAYWHITE)
            
            rl.draw_text("POSITION TEXTURE", 10, screen_height - 30, 20, rl.DARKGREEN)
        
        elif mode == DeferredMode.NORMAL:
            texture = rl.Texture()
            texture.id = gbuffer.normal_texture
            texture.width = screen_width
            texture.height = screen_height
            rl.draw_texture_rec(texture, rl.Rectangle(0, 0, screen_width, -screen_height), rl.Vector2(0, 0), rl.RAYWHITE)
            
            rl.draw_text("NORMAL TEXTURE", 10, screen_height - 30, 20, rl.DARKGREEN)
        
        elif mode == DeferredMode.ALBEDO:
            texture = rl.Texture()
            texture.id = gbuffer.albedo_spec_texture
            texture.width = screen_width
            texture.height = screen_height
            rl.draw_texture_rec(texture, rl.Rectangle(0, 0, screen_width, -screen_height), rl.Vector2(0, 0), rl.RAYWHITE)
            
            rl.draw_text("ALBEDO TEXTURE", 10, screen_height - 30, 20, rl.DARKGREEN)

        rl.draw_text("Toggle lights keys: [Y][R][G][B]", 10, 40, 20, rl.DARKGRAY)
        rl.draw_text("Switch G-buffer textures: [1][2][3][4]", 10, 70, 20, rl.DARKGRAY)

        rl.draw_fps(10, 10)
            
        rl.end_drawing()
        # -----------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(model)     # Unload the models
    rl.unload_model(cube)

    rl.unload_shader(deferred_shader) # Unload shaders
    rl.unload_shader(gbuffer_shader)

    # Unload geometry buffer and all attached textures
    rl.rl_unload_framebuffer(gbuffer.framebuffer)
    rl.rl_unload_texture(gbuffer.position_texture)
    rl.rl_unload_texture(gbuffer.normal_texture)
    rl.rl_unload_texture(gbuffer.albedo_spec_texture)
    rl.rl_unload_texture(gbuffer.depth_renderbuffer)

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()