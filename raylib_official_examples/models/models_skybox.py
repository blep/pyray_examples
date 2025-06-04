"""raylib [models] example - Skybox loading and drawing
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.8, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Define GLSL versions based on platform
GLSL_VERSION = 330
# GLSL_VERSION = 100 #set to 100 for Android, Web.

# Generate cubemap (6 faces) from equirectangular (panorama) texture
def gen_texture_cubemap(shader, panorama, size, format_):
    cubemap = rl.Texture() # rl.TextureCubemap()

    rl.rl_disable_backface_culling()  # Disable backface culling to render inside the cube

    # STEP 1: Setup framebuffer
    #------------------------------------------------------------------------------------------
    rbo = rl.rl_load_texture_depth(size, size, True)
    cubemap.id = rl.rl_load_texture_cubemap(0, size, format_, 1)

    fbo = rl.rl_load_framebuffer()
    rl.rl_framebuffer_attach(fbo, rbo, rl.RL_ATTACHMENT_DEPTH, rl.RL_ATTACHMENT_RENDERBUFFER, 0)
    rl.rl_framebuffer_attach(fbo, cubemap.id, rl.RL_ATTACHMENT_COLOR_CHANNEL0, rl.RL_ATTACHMENT_CUBEMAP_POSITIVE_X, 0)

    # Check if framebuffer is complete with attachments (valid)
    if rl.rl_framebuffer_complete(fbo):
        rl.trace_log(rl.LOG_INFO, f"FBO: [ID {fbo}] Framebuffer object created successfully")
    #------------------------------------------------------------------------------------------

    # STEP 2: Draw to framebuffer
    #------------------------------------------------------------------------------------------
    # NOTE: Shader is used to convert HDR equirectangular environment map to cubemap equivalent (6 faces)
    rl.rl_enable_shader(shader.id)

    # Define projection matrix and send it to shader
    mat_fbo_projection = rl.matrix_perspective(90.0 * rl.DEG2RAD, 1.0, rl.rl_get_cull_distance_near(), rl.rl_get_cull_distance_far())
    rl.rl_set_uniform_matrix(shader.locs[rl.SHADER_LOC_MATRIX_PROJECTION], mat_fbo_projection)

    # Define view matrix for every side of the cubemap
    fbo_views = [
        rl.matrix_look_at(rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(1.0, 0.0, 0.0), rl.Vector3(0.0, -1.0, 0.0)),
        rl.matrix_look_at(rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(-1.0, 0.0, 0.0), rl.Vector3(0.0, -1.0, 0.0)),
        rl.matrix_look_at(rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(0.0, 1.0, 0.0), rl.Vector3(0.0, 0.0, 1.0)),
        rl.matrix_look_at(rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(0.0, -1.0, 0.0), rl.Vector3(0.0, 0.0, -1.0)),
        rl.matrix_look_at(rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(0.0, 0.0, 1.0), rl.Vector3(0.0, -1.0, 0.0)),
        rl.matrix_look_at(rl.Vector3(0.0, 0.0, 0.0), rl.Vector3(0.0, 0.0, -1.0), rl.Vector3(0.0, -1.0, 0.0))
    ]

    rl.rl_viewport(0, 0, size, size)  # Set viewport to current fbo dimensions
    
    # Activate and enable texture for drawing to cubemap faces
    rl.rl_active_texture_slot(0)
    rl.rl_enable_texture(panorama.id)

    for i in range(6):
        # Set the view matrix for the current cube face
        rl.rl_set_uniform_matrix(shader.locs[rl.SHADER_LOC_MATRIX_VIEW], fbo_views[i])
        
        # Select the current cubemap face attachment for the fbo
        # WARNING: This function by default enables->attach->disables fbo!!!
        rl.rl_framebuffer_attach(fbo, cubemap.id, rl.RL_ATTACHMENT_COLOR_CHANNEL0, rl.RL_ATTACHMENT_CUBEMAP_POSITIVE_X + i, 0)
        rl.rl_enable_framebuffer(fbo)

        # Load and draw a cube, it uses the current enabled texture
        rl.rl_clear_screen_buffers()
        rl.rl_load_draw_cube()

    #------------------------------------------------------------------------------------------

    # STEP 3: Unload framebuffer and reset state
    #------------------------------------------------------------------------------------------
    rl.rl_disable_shader()          # Unbind shader
    rl.rl_disable_texture()         # Unbind texture
    rl.rl_disable_framebuffer()     # Unbind framebuffer
    rl.rl_unload_framebuffer(fbo)   # Unload framebuffer (and automatically attached depth texture/renderbuffer)

    # Reset viewport dimensions to default
    rl.rl_viewport(0, 0, rl.rl_get_framebuffer_width(), rl.rl_get_framebuffer_height())
    rl.rl_enable_backface_culling()
    #------------------------------------------------------------------------------------------

    cubemap.width = size
    cubemap.height = size
    cubemap.mipmaps = 1
    cubemap.format = format_

    return cubemap

# Program main entry point
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - skybox loading and drawing")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(1.0, 1.0, 1.0)     # Camera position
    camera.target = rl.Vector3(4.0, 1.0, 4.0)       # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    # Load skybox model
    cube = rl.gen_mesh_cube(1.0, 1.0, 1.0)
    skybox = rl.load_model_from_mesh(cube)

    # Set this to true to use an HDR Texture, Note that raylib must be built with HDR Support for this to work SUPPORT_FILEFORMAT_HDR
    use_hdr = False

    # Load skybox shader and set required locations
    # NOTE: Some locations are automatically set at shader loading
    skybox.materials[0].shader = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/skybox.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/skybox.fs")
    )

    rl.set_shader_value(
        skybox.materials[0].shader, 
        rl.get_shader_location(skybox.materials[0].shader, "environmentMap"), 
        rl.ffi.new("int*", rl.MATERIAL_MAP_CUBEMAP), 
        rl.SHADER_UNIFORM_INT
    )
    rl.set_shader_value(
        skybox.materials[0].shader,
        rl.get_shader_location(skybox.materials[0].shader, "doGamma"),
        rl.ffi.new("int*", 1 if use_hdr else 0),
        rl.SHADER_UNIFORM_INT
    )
    rl.set_shader_value(
        skybox.materials[0].shader,
        rl.get_shader_location(skybox.materials[0].shader, "vflipped"),
        rl.ffi.new("int*", 1 if use_hdr else 0),
        rl.SHADER_UNIFORM_INT
    )

    # Load cubemap shader and setup required shader locations
    shdr_cubemap = rl.load_shader(
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/cubemap.vs"),
        str(THIS_DIR/f"resources/shaders/glsl{GLSL_VERSION}/cubemap.fs")
    )

    rl.set_shader_value(
        shdr_cubemap,
        rl.get_shader_location(shdr_cubemap, "equirectangularMap"),
        rl.ffi.new("int*", 0),
        rl.SHADER_UNIFORM_INT
    )

    skybox_file_name = ""
    
    if use_hdr:
        skybox_file_name = str(THIS_DIR/"resources/dresden_square_2k.hdr")

        # Load HDR panorama (sphere) texture
        panorama = rl.load_texture(skybox_file_name)

        # Generate cubemap (texture with 6 quads-cube-mapping) from panorama HDR texture
        skybox.materials[0].maps[rl.MATERIAL_MAP_CUBEMAP].texture = gen_texture_cubemap(
            shdr_cubemap, panorama, 1024, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
        )

        rl.unload_texture(panorama)  # Texture not required anymore, cubemap already generated
    else:
        img = rl.load_image(str(THIS_DIR/"resources/skybox.png"))
        skybox.materials[0].maps[rl.MATERIAL_MAP_CUBEMAP].texture = rl.load_texture_cubemap(img, rl.CUBEMAP_LAYOUT_AUTO_DETECT)
        rl.unload_image(img)

    rl.disable_cursor()  # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        # Load new cubemap texture on drag&drop
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()

            if dropped_files.count == 1:  # Only support one file dropped
                file_path = dropped_files.paths[0]
                if rl.is_file_extension(file_path, ".png;.jpg;.hdr;.bmp;.tga"):
                    # Unload current cubemap texture to load new one
                    rl.unload_texture(skybox.materials[0].maps[rl.MATERIAL_MAP_CUBEMAP].texture)
                    
                    if use_hdr:
                        # Load HDR panorama (sphere) texture
                        panorama = rl.load_texture(file_path)

                        # Generate cubemap from panorama texture
                        skybox.materials[0].maps[rl.MATERIAL_MAP_CUBEMAP].texture = gen_texture_cubemap(
                            shdr_cubemap, panorama, 1024, rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8
                        )
                        
                        rl.unload_texture(panorama)  # Texture not required anymore, cubemap already generated
                    else:
                        img = rl.load_image(file_path)
                        skybox.materials[0].maps[rl.MATERIAL_MAP_CUBEMAP].texture = rl.load_texture_cubemap(img, rl.CUBEMAP_LAYOUT_AUTO_DETECT)
                        rl.unload_image(img)

                    skybox_file_name = file_path

            rl.unload_dropped_files(dropped_files)  # Unload filepaths from memory
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        # We are inside the cube, we need to disable backface culling!
        rl.rl_disable_backface_culling()
        rl.rl_disable_depth_mask()
        rl.draw_model(skybox, rl.Vector3(0, 0, 0), 1.0, rl.WHITE)
        rl.rl_enable_backface_culling()
        rl.rl_enable_depth_mask()

        rl.draw_grid(10, 1.0)

        rl.end_mode_3d()

        if use_hdr:
            rl.draw_text(f"Panorama image from hdrihaven.com: {rl.get_file_name(skybox_file_name)}", 
                        10, rl.get_screen_height() - 20, 10, rl.BLACK)
        else:
            rl.draw_text(f": {rl.get_file_name(skybox_file_name)}", 
                        10, rl.get_screen_height() - 20, 10, rl.BLACK)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_shader(skybox.materials[0].shader)
    rl.unload_texture(skybox.materials[0].maps[rl.MATERIAL_MAP_CUBEMAP].texture)

    rl.unload_model(skybox)  # Unload skybox model

    rl.close_window()  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
