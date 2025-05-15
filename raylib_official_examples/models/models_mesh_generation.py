"""raylib [models] example - procedural mesh generation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.8, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import ctypes  # For memory allocation

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Parametric 3d shapes to generate
NUM_MODELS = 9

# Generate a simple triangle mesh from code
def gen_mesh_custom():
    mesh = rl.Mesh()
    mesh.triangleCount = 1
    mesh.vertexCount = mesh.triangleCount * 3
    
    # Allocate memory for vertices, texcoords, and normals
    # In Python, we can use list comprehension to initialize these arrays
    vertices_size = mesh.vertexCount * 3
    texcoords_size = mesh.vertexCount * 2
    normals_size = mesh.vertexCount * 3
    
    # Initialize arrays with zeros
    vertices = [0.0] * vertices_size
    texcoords = [0.0] * texcoords_size
    normals = [0.0] * normals_size

    # Vertex at (0, 0, 0)
    vertices[0] = 0.0
    vertices[1] = 0.0
    vertices[2] = 0.0
    normals[0] = 0.0
    normals[1] = 1.0
    normals[2] = 0.0
    texcoords[0] = 0.0
    texcoords[1] = 0.0

    # Vertex at (1, 0, 2)
    vertices[3] = 1.0
    vertices[4] = 0.0
    vertices[5] = 2.0
    normals[3] = 0.0
    normals[4] = 1.0
    normals[5] = 0.0
    texcoords[2] = 0.5
    texcoords[3] = 1.0

    # Vertex at (2, 0, 0)
    vertices[6] = 2.0
    vertices[7] = 0.0
    vertices[8] = 0.0
    normals[6] = 0.0
    normals[7] = 1.0
    normals[8] = 0.0
    texcoords[4] = 1.0
    texcoords[5] = 0.0
    
    # Assign data to mesh
    mesh.vertices = vertices
    mesh.texcoords = texcoords
    mesh.normals = normals
    
    # Upload mesh data from CPU (RAM) to GPU (VRAM) memory
    rl.upload_mesh(mesh, False)
    
    return mesh

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - mesh generation")

    # We generate a checked image for texturing
    checked = rl.gen_image_checked(2, 2, 1, 1, rl.RED, rl.GREEN)
    texture = rl.load_texture_from_image(checked)
    rl.unload_image(checked)

    models = [None] * NUM_MODELS

    models[0] = rl.load_model_from_mesh(rl.gen_mesh_plane(2, 2, 4, 3))
    models[1] = rl.load_model_from_mesh(rl.gen_mesh_cube(2.0, 1.0, 2.0))
    models[2] = rl.load_model_from_mesh(rl.gen_mesh_sphere(2, 32, 32))
    models[3] = rl.load_model_from_mesh(rl.gen_mesh_hemi_sphere(2, 16, 16))
    models[4] = rl.load_model_from_mesh(rl.gen_mesh_cylinder(1, 2, 16))
    models[5] = rl.load_model_from_mesh(rl.gen_mesh_torus(0.25, 4.0, 16, 32))
    models[6] = rl.load_model_from_mesh(rl.gen_mesh_knot(1.0, 2.0, 16, 128))
    models[7] = rl.load_model_from_mesh(rl.gen_mesh_poly(5, 2.0))
    models[8] = rl.load_model_from_mesh(gen_mesh_custom())
    
    # Generated meshes could be exported as .obj files
    #rl.export_mesh(models[0].meshes[0], "plane.obj")
    #rl.export_mesh(models[1].meshes[0], "cube.obj")
    #rl.export_mesh(models[2].meshes[0], "sphere.obj")
    #rl.export_mesh(models[3].meshes[0], "hemisphere.obj")
    #rl.export_mesh(models[4].meshes[0], "cylinder.obj")
    #rl.export_mesh(models[5].meshes[0], "torus.obj")
    #rl.export_mesh(models[6].meshes[0], "knot.obj")
    #rl.export_mesh(models[7].meshes[0], "poly.obj")
    #rl.export_mesh(models[8].meshes[0], "custom.obj")

    # Set checked texture as default diffuse component for all models material
    for i in range(NUM_MODELS):
        rl.set_material_texture(models[i].materials[0], rl.MATERIAL_MAP_DIFFUSE, texture)

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(5.0, 5.0, 5.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    # Model drawing position
    position = rl.Vector3(0.0, 0.0, 0.0)

    current_model = 0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        rl.update_camera(camera, rl.CAMERA_ORBITAL)

        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            current_model = (current_model + 1) % NUM_MODELS  # Cycle between the textures

        if rl.is_key_pressed(rl.KEY_RIGHT):
            current_model += 1
            if current_model >= NUM_MODELS:
                current_model = 0
        elif rl.is_key_pressed(rl.KEY_LEFT):
            current_model -= 1
            if current_model < 0:
                current_model = NUM_MODELS - 1
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        rl.draw_model(models[current_model], position, 1.0, rl.WHITE)
        rl.draw_grid(10, 1.0)

        rl.end_mode_3d()

        rl.draw_rectangle(30, 400, 310, 30, rl.fade(rl.SKYBLUE, 0.5))
        rl.draw_rectangle_lines(30, 400, 310, 30, rl.fade(rl.DARKBLUE, 0.5))
        rl.draw_text("MOUSE LEFT BUTTON to CYCLE PROCEDURAL MODELS", 40, 410, 10, rl.BLUE)

        if current_model == 0:
            rl.draw_text("PLANE", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 1:
            rl.draw_text("CUBE", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 2:
            rl.draw_text("SPHERE", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 3:
            rl.draw_text("HEMISPHERE", 640, 10, 20, rl.DARKBLUE)
        elif current_model == 4:
            rl.draw_text("CYLINDER", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 5:
            rl.draw_text("TORUS", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 6:
            rl.draw_text("KNOT", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 7:
            rl.draw_text("POLY", 680, 10, 20, rl.DARKBLUE)
        elif current_model == 8:
            rl.draw_text("Custom (triangle)", 580, 10, 20, rl.DARKBLUE)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_texture(texture)  # Unload texture

    # Unload models data (GPU VRAM)
    for i in range(NUM_MODELS):
        rl.unload_model(models[i])

    rl.close_window()          # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
