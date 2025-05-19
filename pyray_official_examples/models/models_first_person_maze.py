"""raylib [models] example - first person maze
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib [models] example - first person maze")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.2, 0.4, 0.2)    # Camera position
    camera.target = rl.Vector3(0.185, 0.4, 0.0)    # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)          # Camera up vector (rotation towards target)
    camera.fovy = 45.0                             # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE      # Camera projection type

    im_map = rl.load_image(str(THIS_DIR/"resources/cubicmap.png"))      # Load cubicmap image (RAM)
    cubicmap = rl.load_texture_from_image(im_map)       # Convert image to texture to display (VRAM)
    mesh = rl.gen_mesh_cubicmap(im_map, rl.Vector3(1.0, 1.0, 1.0))
    model = rl.load_model_from_mesh(mesh)

    # NOTE: By default each cube is mapped to one part of texture atlas
    texture = rl.load_texture(str(THIS_DIR/"resources/cubicmap_atlas.png"))    # Load map texture
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture    # Set map diffuse texture

    # Get map image data to be used for collision detection
    map_pixels = rl.load_image_colors(im_map)
    rl.unload_image(im_map)             # Unload image from RAM

    map_position = rl.Vector3(-16.0, 0.0, -8.0)  # Set model position

    rl.disable_cursor()                # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        old_cam_pos = camera.position    # Store old camera position

        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        # Check player collision (we simplify to 2D collision detection)
        player_pos = rl.Vector2(camera.position.x, camera.position.z)
        player_radius = 0.1  # Collision radius (player is modelled as a cilinder for collision)

        player_cell_x = int(player_pos.x - map_position.x + 0.5)
        player_cell_y = int(player_pos.y - map_position.z + 0.5)

        # Out-of-limits security check
        if player_cell_x < 0:
            player_cell_x = 0
        elif player_cell_x >= cubicmap.width:
            player_cell_x = cubicmap.width - 1

        if player_cell_y < 0:
            player_cell_y = 0
        elif player_cell_y >= cubicmap.height:
            player_cell_y = cubicmap.height - 1

        # Check map collisions using image data and player position
        # TODO: Improvement: Just check player surrounding cells for collision
        for y in range(cubicmap.height):
            for x in range(cubicmap.width):
                if (rl.get_pixel_color(map_pixels[y*cubicmap.width + x], rl.PIXELFORMAT_UNCOMPRESSED_R8G8B8A8).r == 255 and  # Collision: white pixel, only check R channel
                    rl.check_collision_circle_rec(
                        player_pos, player_radius,
                        rl.Rectangle(map_position.x - 0.5 + x*1.0, map_position.z - 0.5 + y*1.0, 1.0, 1.0))):
                    # Collision detected, reset camera position
                    camera.position = old_cam_pos
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)
        rl.draw_model(model, map_position, 1.0, rl.WHITE)  # Draw maze map
        rl.end_mode_3d()

        rl.draw_texture_ex(cubicmap, rl.Vector2(rl.get_screen_width() - cubicmap.width*4.0 - 20, 20.0), 0.0, 4.0, rl.WHITE)
        rl.draw_rectangle_lines(rl.get_screen_width() - cubicmap.width*4 - 20, 20, cubicmap.width*4, cubicmap.height*4, rl.GREEN)

        # Draw player position radar
        rl.draw_rectangle(rl.get_screen_width() - cubicmap.width*4 - 20 + player_cell_x*4, 20 + player_cell_y*4, 4, 4, rl.RED)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_image_colors(map_pixels)   # Unload color array

    rl.unload_texture(cubicmap)        # Unload cubicmap texture
    rl.unload_texture(texture)         # Unload map texture
    rl.unload_model(model)             # Unload map model

    rl.close_window()                  # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
