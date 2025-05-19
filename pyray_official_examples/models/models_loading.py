"""raylib [models] example - Models loading
Example complexity rating: [★☆☆☆] 1/4
NOTE: raylib supports multiple models file formats:
  - OBJ  > Text file format. Must include vertex position-texcoords-normals information,
           if files references some .mtl materials file, it will be loaded (or try to).
  - GLTF > Text/binary file format. Includes lot of information and it could
           also reference external files, raylib will try loading mesh and materials data.
  - IQM  > Binary file format. Includes mesh vertex data but also animation data,
           raylib can load .iqm animations.
  - VOX  > Binary file format. MagikaVoxel mesh format:
           https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt
  - M3D  > Binary file format. Model 3D format:
           https://bztsrc.gitlab.io/model3d
Example originally created with raylib 2.0, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

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

    rl.init_window(screen_width, screen_height, "raylib [models] example - models loading")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(50.0, 50.0, 50.0)  # Camera position
    camera.target = rl.Vector3(0.0, 10.0, 0.0)      # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.0, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 45.0                              # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE       # Camera mode type

    model = rl.load_model(str(THIS_DIR/"resources/models/obj/castle.obj"))  # Load model
    texture = rl.load_texture(str(THIS_DIR/"resources/models/obj/castle_diffuse.png"))  # Load model texture
    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture       # Set map diffuse texture

    position = rl.Vector3(0.0, 0.0, 0.0)                    # Set model position

    bounds = rl.get_mesh_bounding_box(model.meshes[0])      # Set model bounds

    # NOTE: bounds are calculated from the original size of the model,
    # if model is scaled on drawing, bounds must be also scaled

    selected = False          # Selected object flag

    rl.disable_cursor()       # Limit cursor to relative movement inside the window

    rl.set_target_fps(60)     # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)

        # Load new models/textures on drag&drop
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()

            if dropped_files.count == 1:  # Only support one file dropped
                file_path = dropped_files.paths[0]

                if (rl.is_file_extension(file_path, ".obj") or
                    rl.is_file_extension(file_path, ".gltf") or
                    rl.is_file_extension(file_path, ".glb") or
                    rl.is_file_extension(file_path, ".vox") or
                    rl.is_file_extension(file_path, ".iqm") or
                    rl.is_file_extension(file_path, ".m3d")):  # Model file formats supported
                    
                    rl.unload_model(model)             # Unload previous model
                    model = rl.load_model(file_path)   # Load new model
                    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture  # Set current map diffuse texture

                    bounds = rl.get_mesh_bounding_box(model.meshes[0])

                    # TODO: Move camera position from target enough distance to visualize model properly
                elif rl.is_file_extension(file_path, ".png"):  # Texture file formats supported
                    # Unload current model texture and load new one
                    rl.unload_texture(texture)
                    texture = rl.load_texture(file_path)
                    model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture

            rl.unload_dropped_files(dropped_files)    # Unload filepaths from memory

        # Select model on mouse click
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            # Check collision between ray and box
            ray_collision = rl.get_ray_collision_box(
                rl.get_screen_to_world_ray(rl.get_mouse_position(), camera), 
                bounds
            )
            if ray_collision.hit:
                selected = not selected
            else:
                selected = False
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_model(model, position, 1.0, rl.WHITE)  # Draw 3d model with texture

        rl.draw_grid(20, 10.0)  # Draw a grid

        if selected:
            rl.draw_bounding_box(bounds, rl.GREEN)   # Draw selection box

        rl.end_mode_3d()

        rl.draw_text("Drag & drop model to load mesh/texture.", 10, rl.get_screen_height() - 20, 10, rl.DARKGRAY)
        if selected:
            rl.draw_text("MODEL SELECTED", rl.get_screen_width() - 110, 10, 10, rl.GREEN)

        rl.draw_text("(c) Castle 3D model by Alberto Cano", screen_width - 200, screen_height - 20, 10, rl.GRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture)  # Unload texture
    rl.unload_model(model)      # Unload model

    rl.close_window()           # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
