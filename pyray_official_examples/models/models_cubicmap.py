"""raylib [models] example - Cubicmap loading and drawing
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.8, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Program main entry point
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - cubesmap loading and drawing")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(16.0, 14.0, 16.0)      # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)           # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)               # Camera up vector (rotation towards target)
    camera.fovy = 45.0                                  # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE           # Camera projection type

    image = rl.load_image(str(THIS_DIR/"resources/cubicmap.png"))      # Load cubicmap image (RAM)
    cubicmap = rl.load_texture_from_image(image)       # Convert image to texture to display (VRAM)

    mesh = rl.gen_mesh_cubicmap(image, rl.Vector3(1.0, 1.0, 1.0))
    model = rl.load_model_from_mesh(mesh)

    # NOTE: By default each cube is mapped to one part of texture atlas
    texture = rl.load_texture(str(THIS_DIR/"resources/cubicmap_atlas.png"))    # Load map texture
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture    # Set map diffuse texture

    map_position = rl.Vector3(-16.0, 0.0, -8.0)          # Set model position

    rl.unload_image(image)     # Unload cubesmap image from RAM, already uploaded to VRAM

    pause = False     # Pause camera orbital rotation (and zoom)

    rl.set_target_fps(60)                   # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():        # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if rl.is_key_pressed(rl.KEY_P): 
            pause = not pause

        if not pause: 
            rl.update_camera(camera, rl.CAMERA_ORBITAL)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_model(model, map_position, 1.0, rl.WHITE)

        rl.end_mode_3d()

        rl.draw_texture_ex(cubicmap, rl.Vector2(screen_width - cubicmap.width*4.0 - 20, 20.0), 0.0, 4.0, rl.WHITE)
        rl.draw_rectangle_lines(screen_width - cubicmap.width*4 - 20, 20, cubicmap.width*4, cubicmap.height*4, rl.GREEN)

        rl.draw_text("cubicmap image used to", 658, 90, 10, rl.GRAY)
        rl.draw_text("generate map 3d model", 658, 104, 10, rl.GRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(cubicmap)    # Unload cubicmap texture
    rl.unload_texture(texture)     # Unload map texture
    rl.unload_model(model)         # Unload map model

    rl.close_window()              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
