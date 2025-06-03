"""raylib [shaders] example - lightmap
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires raylib OpenGL 3.3 or ES2 versions for shaders support,
      OpenGL 1.1 does not support shaders, recompile raylib to OpenGL 3.3 version.
NOTE: Shaders used in this example are #version 330 (OpenGL 3.3).
Example originally created with raylib 4.5, last time updated with raylib 4.5
Example contributed by Jussi Viitala (@nullstare) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Jussi Viitala (@nullstare) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import ctypes

THIS_DIR = Path(__file__).resolve().parent

# Check if platform is web or desktop
if rl.is_window_fullscreen():  # This is a simple way to check if we're on web (fullscreen by default)
    GLSL_VERSION = 100
else:
    GLSL_VERSION = 330

MAP_SIZE = 10

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)  # Enable Multi Sampling Anti Aliasing 4x (if available)
    rl.init_window(screen_width, screen_height, "raylib [shaders] example - lightmap")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(4.0, 6.0, 8.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    mesh = rl.gen_mesh_plane(MAP_SIZE, MAP_SIZE, 1, 1)

    # GenMeshPlane doesn't generate texcoords2 so we will upload them separately
    texcoords2 = [
        0.0, 0.0,  # First vertex
        1.0, 0.0,  # Second vertex
        0.0, 1.0,  # Third vertex
        1.0, 1.0  # Fourth vertex
    ]
    mesh.texcoords2 = rl.ffi.new("float[]", texcoords2)

    # Load a new texcoords2 attributes buffer
    mesh.vboId[rl.SHADER_LOC_VERTEX_TEXCOORD02] = rl.rl_load_vertex_buffer(
        mesh.texcoords2, rl.ffi.sizeof("float") * len(texcoords2), False)
    rl.rl_enable_vertex_array(mesh.vaoId)
    
    # Index 5 is for texcoords2
    rl.rl_set_vertex_attribute(5, 2, rl.RL_FLOAT, 0, 0, 0)
    rl.rl_enable_vertex_attribute(5)
    rl.rl_disable_vertex_array()

    # Load lightmap shader
    shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/lightmap.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/lightmap.fs")
    )

    texture = rl.load_texture(str(THIS_DIR/"resources/cubicmap_atlas.png"))
    light = rl.load_texture(str(THIS_DIR/"resources/spark_flame.png"))

    rl.gen_texture_mipmaps(texture)
    rl.set_texture_filter(texture, rl.TEXTURE_FILTER_TRILINEAR)

    lightmap = rl.load_render_texture(MAP_SIZE, MAP_SIZE)

    rl.set_texture_filter(lightmap.texture, rl.TEXTURE_FILTER_TRILINEAR)

    material = rl.load_material_default()
    material.shader = shader
    material.maps[rl.MATERIAL_MAP_ALBEDO].texture = texture
    material.maps[rl.MATERIAL_MAP_METALNESS].texture = lightmap.texture

    # Drawing to lightmap
    rl.begin_texture_mode(lightmap)
    rl.clear_background(rl.BLACK)

    rl.begin_blend_mode(rl.BLEND_ADDITIVE)
    rl.draw_texture_pro(
        light,
        rl.Rectangle(0, 0, light.width, light.height),
        rl.Rectangle(0, 0, 20, 20),
        rl.Vector2(10.0, 10.0),
        0.0,
        rl.RED
    )
    rl.draw_texture_pro(
        light,
        rl.Rectangle(0, 0, light.width, light.height),
        rl.Rectangle(8, 4, 20, 20),
        rl.Vector2(10.0, 10.0),
        0.0,
        rl.BLUE
    )
    rl.draw_texture_pro(
        light,
        rl.Rectangle(0, 0, light.width, light.height),
        rl.Rectangle(8, 8, 10, 10),
        rl.Vector2(5.0, 5.0),
        0.0,
        rl.GREEN
    )
    rl.begin_blend_mode(rl.BLEND_ALPHA)
    rl.end_texture_mode()

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
        rl.draw_mesh(mesh, material, rl.matrix_identity())
        rl.end_mode_3d()

        rl.draw_fps(10, 10)
        rl.draw_texture_pro(
            lightmap.texture,
            rl.Rectangle(0, 0, -MAP_SIZE, -MAP_SIZE),
            rl.Rectangle(rl.get_render_width() - MAP_SIZE*8 - 10, 10, MAP_SIZE*8, MAP_SIZE*8),
            rl.Vector2(0.0, 0.0),
            0.0,
            rl.WHITE
        )
            
        rl.draw_text("lightmap", rl.get_render_width() - 66, 16 + MAP_SIZE*8, 10, rl.GRAY)
        rl.draw_text("10x10 pixels", rl.get_render_width() - 76, 30 + MAP_SIZE*8, 10, rl.GRAY)
            
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_mesh(mesh)       # Unload the mesh
    rl.unload_shader(shader)   # Unload shader
    rl.unload_texture(texture) # Unload texture
    rl.unload_texture(light)   # Unload texture
    rl.rl_free(mesh_texcoords2_ptr)  # Free manually allocated memory for texcoords2

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()