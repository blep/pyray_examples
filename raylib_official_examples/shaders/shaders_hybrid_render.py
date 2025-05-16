"""raylib [shaders] example - Hybrid Rendering
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example contributed by Buğra Alptekin Sarı (@BugraAlptekinSari) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Buğra Alptekin Sarı (@BugraAlptekinSari)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math
from pathlib import Path
from dataclasses import dataclass

THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

#------------------------------------------------------------------------------------
# Declare custom Structs
#------------------------------------------------------------------------------------
@dataclass
class RayLocs:
    camPos: int = 0
    camDir: int = 0
    screenCenter: int = 0

#------------------------------------------------------------------------------------
# Define custom functions required for the example
#------------------------------------------------------------------------------------
# Load custom render texture, create a writable depth texture buffer
def load_render_texture_depth_tex(width, height):
    target = rl.RenderTexture()

    target.id = rl.rl_load_framebuffer()  # Load an empty framebuffer

    if target.id > 0:
        rl.rl_enable_framebuffer(target.id)

        # Create color texture (default to RGBA)
        target.texture.id = rl.rl_load_texture(None, width, height, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8, 1)
        target.texture.width = width
        target.texture.height = height
        target.texture.format = rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
        target.texture.mipmaps = 1

        # Create depth texture buffer (instead of raylib default renderbuffer)
        target.depth.id = rl.rl_load_texture_depth(width, height, False)
        target.depth.width = width
        target.depth.height = height
        target.depth.format = 19       #DEPTH_COMPONENT_24BIT?
        target.depth.mipmaps = 1

        # Attach color texture and depth texture to FBO
        rl.rl_framebuffer_attach(target.id, target.texture.id, rl.RL_ATTACHMENT_COLOR_CHANNEL0, rl.RL_ATTACHMENT_TEXTURE2D, 0)
        rl.rl_framebuffer_attach(target.id, target.depth.id, rl.RL_ATTACHMENT_DEPTH, rl.RL_ATTACHMENT_TEXTURE2D, 0)

        # Check if fbo is complete with attachments (valid)
        if rl.rl_framebuffer_complete(target.id):
            rl.trace_log(rl.LOG_INFO, f"FBO: [ID {target.id}] Framebuffer object created successfully")

        rl.rl_disable_framebuffer()
    else:
        rl.trace_log(rl.LOG_WARNING, "FBO: Framebuffer object can not be created")

    return target

# Unload render texture from GPU memory (VRAM)
def unload_render_texture_depth_tex(target):
    if target.id > 0:
        # Color texture attached to FBO is deleted
        rl.rl_unload_texture(target.texture.id)
        rl.rl_unload_texture(target.depth.id)

        # NOTE: Depth texture is automatically
        # queried and deleted before deleting framebuffer
        rl.rl_unload_framebuffer(target.id)

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shaders] example - hybrid rendering")

    # This Shader calculates pixel depth and color using raymarch
    shdr_raymarch = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/hybrid_raymarch.fs"))

    # This Shader is a standard rasterization fragment shader with the addition of depth writing
    # You are required to write depth for all shaders if one shader does it
    shdr_raster = rl.load_shader("", str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/hybrid_raster.fs"))

    # Declare Struct used to store camera locs.
    march_locs = RayLocs()

    # Fill the struct with shader locs.
    march_locs.camPos = rl.get_shader_location(shdr_raymarch, "camPos")
    march_locs.camDir = rl.get_shader_location(shdr_raymarch, "camDir")
    march_locs.screenCenter = rl.get_shader_location(shdr_raymarch, "screenCenter")

    # Transfer screenCenter position to shader. Which is used to calculate ray direction. 
    screen_center = rl.Vector2(screen_width/2.0, screen_height/2.0)
    rl.set_shader_value(shdr_raymarch, march_locs.screenCenter, rl.ffi.new("Vector2 *", [screen_center.x, screen_center.y]), rl.SHADER_UNIFORM_VEC2)

    # Use Customized function to create writable depth texture buffer
    target = load_render_texture_depth_tex(screen_width, screen_height)

    # Define the camera to look into our 3d world
    camera = rl.Camera3D(
        position=rl.Vector3(0.5, 1.0, 1.5),    # Camera position
        target=rl.Vector3(0.0, 0.5, 0.0),      # Camera looking at point
        up=rl.Vector3(0.0, 1.0, 0.0),          # Camera up vector (rotation towards target)
        fovy=45.0,                             # Camera field-of-view Y
        projection=rl.CAMERA_PERSPECTIVE       # Camera projection type
    )
    
    # Camera FOV is pre-calculated in the camera Distance.
    cam_dist = 1.0/(math.tan(camera.fovy*0.5*rl.DEG2RAD))
    
    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(rl.byref(camera), rl.CAMERA_ORBITAL)

        # Update Camera Postion in the ray march shader.
        rl.set_shader_value(shdr_raymarch, march_locs.camPos, rl.ffi.new("Vector3 *", [camera.position.x, camera.position.y, camera.position.z]), rl.SHADER_UNIFORM_VEC3)
        
        # Update Camera Looking Vector. Vector length determines FOV.
        camDir = rl.vector3_scale(
            rl.vector3_normalize(
                rl.vector3_subtract(camera.target, camera.position)
            ), 
            cam_dist
        )
        rl.set_shader_value(shdr_raymarch, march_locs.camDir, rl.ffi.new("Vector3 *", [camDir.x, camDir.y, camDir.z]), rl.SHADER_UNIFORM_VEC3)
        #----------------------------------------------------------------------------------
        
        # Draw
        #----------------------------------------------------------------------------------
        # Draw into our custom render texture (framebuffer)
        rl.begin_texture_mode(target)
        rl.clear_background(rl.WHITE)

        # Raymarch Scene
        rl.rl_enable_depth_test() #Manually enable Depth Test to handle multiple rendering methods.
        rl.begin_shader_mode(shdr_raymarch)
        rl.draw_rectangle_rec(rl.Rectangle(0, 0, screen_width, screen_height), rl.WHITE)
        rl.end_shader_mode()
            
        # Rasterize Scene
        rl.begin_mode_3d(camera)
        rl.begin_shader_mode(shdr_raster)
        rl.draw_cube_wires_v(rl.Vector3(0.0, 0.5, 1.0), rl.Vector3(1.0, 1.0, 1.0), rl.RED)
        rl.draw_cube_v(rl.Vector3(0.0, 0.5, 1.0), rl.Vector3(1.0, 1.0, 1.0), rl.PURPLE)
        rl.draw_cube_wires_v(rl.Vector3(0.0, 0.5, -1.0), rl.Vector3(1.0, 1.0, 1.0), rl.DARKGREEN)
        rl.draw_cube_v(rl.Vector3(0.0, 0.5, -1.0), rl.Vector3(1.0, 1.0, 1.0), rl.YELLOW)
        rl.draw_grid(10, 1.0)
        rl.end_shader_mode()
        rl.end_mode_3d()
        rl.end_texture_mode()

        # Draw into screen our custom render texture 
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        
        rl.draw_texture_rec(target.texture, rl.Rectangle(0, 0, screen_width, -screen_height), rl.Vector2(0, 0), rl.WHITE)
        rl.draw_fps(10, 10)
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    unload_render_texture_depth_tex(target)
    rl.unload_shader(shdr_raymarch)
    rl.unload_shader(shdr_raster)

    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()