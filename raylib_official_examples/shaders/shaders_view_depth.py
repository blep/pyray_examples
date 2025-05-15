"""raylib [shader] example - render depth texture
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.6-dev, last time updated with raylib 5.6-dev
Example contributed by Luís Almeida (@luis605)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2025 Luís Almeida (@luis605)

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

def load_render_texture_with_depth(width, height):
    target = rl.RenderTexture2D()

    target.id = rl.rl_load_framebuffer()  # Load an empty framebuffer

    if target.id > 0:
        rl.rl_enable_framebuffer(target.id)

        # Create color texture (default to RGBA)
        target.texture.id = rl.rl_load_texture(None, width, height, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8, 1)
        target.texture.width = width
        target.texture.height = height
        target.texture.format = rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
        target.texture.mipmaps = 1

        # Create depth texture
        target.depth.id = rl.rl_load_texture_depth(width, height, False)
        target.depth.width = width
        target.depth.height = height
        target.depth.format = 19  # DEPTH_COMPONENT_24BIT? THIS DOESN'T EXIST IN RAYLIB
        target.depth.mipmaps = 1

        # Attach color texture and depth texture to FBO
        rl.rl_framebuffer_attach(target.id, target.texture.id, rl.RL_ATTACHMENT_COLOR_CHANNEL0, rl.RL_ATTACHMENT_TEXTURE2D, 0)
        rl.rl_framebuffer_attach(target.id, target.depth.id, rl.RL_ATTACHMENT_DEPTH, rl.RL_ATTACHMENT_TEXTURE2D, 0)

        # Check if fbo is complete with attachments (valid)
        if rl.rl_framebuffer_complete(target.id):
            rl.tracelog(rl.LOG_INFO, f"FBO: [ID {target.id}] Framebuffer object created successfully")

        rl.rl_disable_framebuffer()
    else:
        rl.tracelog(rl.LOG_WARNING, "FBO: Framebuffer object can not be created")

    return target

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shader] example - render depth texture")

    # Init camera
    camera = rl.Camera3D()
    camera.position = rl.Vector3(4.0, 1.0, 5.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    # Load an empty render texture with a depth texture
    target = load_render_texture_with_depth(screen_width, screen_height)

    # Load depth shader and get depth texture shader location
    depth_shader = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/depth.fs"))
    depth_loc = rl.get_shader_location(depth_shader, "depthTexture")
    flip_texture_loc = rl.get_shader_location(depth_shader, "flipY")
    rl.set_shader_value(depth_shader, flip_texture_loc, rl.ffi.new("int *", 1), rl.SHADER_UNIFORM_INT)  # Flip Y texture

    # Load models
    cube = rl.load_model_from_mesh(rl.gen_mesh_cube(1.0, 1.0, 1.0))
    floor = rl.load_model_from_mesh(rl.gen_mesh_plane(20.0, 20.0, 1, 1))

    rl.disable_cursor()  # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.byref(camera), rl.CAMERA_FREE)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_texture_mode(target)
        rl.clear_background(rl.WHITE)
        
        rl.begin_mode_3d(camera)
        rl.draw_model(cube, rl.Vector3(0.0, 0.0, 0.0), 3.0, rl.YELLOW)
        rl.draw_model(floor, rl.Vector3(10.0, 0.0, 2.0), 2.0, rl.RED)
        rl.end_mode_3d()
        rl.end_texture_mode()

        rl.begin_drawing()

        rl.begin_shader_mode(depth_shader)
        rl.set_shader_value_texture(depth_shader, depth_loc, target.depth)
        rl.draw_texture(target.depth, 0, 0, rl.WHITE)
        rl.end_shader_mode()

        rl.draw_rectangle(10, 10, 320, 93, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(10, 10, 320, 93, rl.BLUE)

        rl.draw_text("Camera Controls:", 20, 20, 10, rl.BLACK)
        rl.draw_text("- WASD to move", 40, 40, 10, rl.DARKGRAY)
        rl.draw_text("- Mouse Wheel Pressed to Pan", 40, 60, 10, rl.DARKGRAY)
        rl.draw_text("- Z to zoom to (0, 0, 0)", 40, 80, 10, rl.DARKGRAY)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(cube)              # Unload model
    rl.unload_model(floor)             # Unload model
    rl.unload_render_texture(target)   # Unload render texture
    rl.unload_shader(depth_shader)     # Unload shader

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()