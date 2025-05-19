"""raylib [models] example - Heightmap loading and drawing
Example complexity rating: [★☆☆☆] 1/4
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

    rl.init_window(screen_width, screen_height, "raylib [models] example - heightmap loading and drawing")

    # Define our custom camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(18.0, 21.0, 18.0)    # Camera position
    camera.target = rl.Vector3(0.0, 0.0, 0.0)         # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)             # Camera up vector (rotation towards target)
    camera.fovy = 45.0                                # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE         # Camera projection type

    image = rl.load_image(str(THIS_DIR/"resources/heightmap.png"))     # Load heightmap image (RAM)
    texture = rl.load_texture_from_image(image)        # Convert image to texture (VRAM)

    mesh = rl.gen_mesh_heightmap(image, rl.Vector3(16, 8, 16))  # Generate heightmap mesh (RAM and VRAM)
    model = rl.load_model_from_mesh(mesh)              # Load model from generated mesh

    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture  # Set map diffuse texture
    map_position = rl.Vector3(-8.0, 0.0, -8.0)         # Define model position

    rl.unload_image(image)  # Unload heightmap image from RAM, already uploaded to VRAM

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_model(model, map_position, 1.0, rl.RED)

        rl.draw_grid(20, 1.0)

        rl.end_mode_3d()

        rl.draw_texture(texture, screen_width - texture.width - 20, 20, rl.WHITE)
        rl.draw_rectangle_lines(screen_width - texture.width - 20, 20, texture.width, texture.height, rl.GREEN)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture)  # Unload texture
    rl.unload_model(model)      # Unload model

    rl.close_window()           # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
