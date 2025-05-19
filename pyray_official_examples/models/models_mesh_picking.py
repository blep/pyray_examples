"""raylib [models] example - Mesh picking in 3d mode, ground plane, triangle, mesh
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 1.7, last time updated with raylib 4.0
Example contributed by Joel Davis (@joeld42) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2017-2025 Joel Davis (@joeld42) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import sys

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

# Define FLT_MAX
FLT_MAX = 340282346638528859811704183484516925440.0  # Maximum value of a float

# Program main entry point
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - mesh picking")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(20.0, 20.0, 20.0)  # Camera position
    camera.target = rl.Vector3(0.0, 8.0, 0.0)       # Camera looking at point
    camera.up = rl.Vector3(0.0, 1.6, 0.0)           # Camera up vector (rotation towards target)
    camera.fovy = 45.0                              # Camera field-of-view Y
    camera.projection = rl.CAMERA_PERSPECTIVE       # Camera projection type

    ray = rl.Ray()  # Picking ray

    tower = rl.load_model(str(THIS_DIR/"resources/models/obj/turret.obj"))  # Load OBJ model
    texture = rl.load_texture(str(THIS_DIR/"resources/models/obj/turret_diffuse.png"))  # Load model texture
    tower.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = texture  # Set model diffuse texture

    tower_pos = rl.Vector3(0.0, 0.0, 0.0)  # Set model position
    tower_bbox = rl.get_mesh_bounding_box(tower.meshes[0])  # Get mesh bounding box

    # Ground quad
    g0 = rl.Vector3(-50.0, 0.0, -50.0)
    g1 = rl.Vector3(-50.0, 0.0, 50.0)
    g2 = rl.Vector3(50.0, 0.0, 50.0)
    g3 = rl.Vector3(50.0, 0.0, -50.0)

    # Test triangle
    ta = rl.Vector3(-25.0, 0.5, 0.0)
    tb = rl.Vector3(-4.0, 2.5, 1.0)
    tc = rl.Vector3(-8.0, 6.5, 0.0)

    bary = rl.Vector3(0.0, 0.0, 0.0)

    # Test sphere
    sp = rl.Vector3(-30.0, 5.0, 5.0)
    sr = 4.0

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if rl.is_cursor_hidden():
            rl.update_camera(camera, rl.CAMERA_FIRST_PERSON)  # Update camera

        # Toggle camera controls
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
            if rl.is_cursor_hidden():
                rl.enable_cursor()
            else:
                rl.disable_cursor()

        # Display information about closest hit
        collision = rl.RayCollision()
        hit_object_name = "None"
        collision.distance = FLT_MAX
        collision.hit = False
        cursor_color = rl.WHITE

        # Get ray and test against objects
        ray = rl.get_screen_to_world_ray(rl.get_mouse_position(), camera)

        # Check ray collision against ground quad
        ground_hit_info = rl.get_ray_collision_quad(ray, g0, g1, g2, g3)

        if ground_hit_info.hit and ground_hit_info.distance < collision.distance:
            collision = ground_hit_info
            cursor_color = rl.GREEN
            hit_object_name = "Ground"

        # Check ray collision against test triangle
        tri_hit_info = rl.get_ray_collision_triangle(ray, ta, tb, tc)

        if tri_hit_info.hit and tri_hit_info.distance < collision.distance:
            collision = tri_hit_info
            cursor_color = rl.PURPLE
            hit_object_name = "Triangle"

            bary = rl.vector3_barycenter(collision.point, ta, tb, tc)

        # Check ray collision against test sphere
        sphere_hit_info = rl.get_ray_collision_sphere(ray, sp, sr)

        if sphere_hit_info.hit and sphere_hit_info.distance < collision.distance:
            collision = sphere_hit_info
            cursor_color = rl.ORANGE
            hit_object_name = "Sphere"

        # Check ray collision against bounding box first, before trying the full ray-mesh test
        box_hit_info = rl.get_ray_collision_box(ray, tower_bbox)

        if box_hit_info.hit and box_hit_info.distance < collision.distance:
            collision = box_hit_info
            cursor_color = rl.ORANGE
            hit_object_name = "Box"

            # Check ray collision against model meshes
            mesh_hit_info = rl.RayCollision()
            for m in range(tower.meshCount):
                # NOTE: We consider the model.transform for the collision check but
                # it can be checked against any transform Matrix, used when checking against same
                # model drawn multiple times with multiple transforms
                mesh_hit_info = rl.get_ray_collision_mesh(ray, tower.meshes[m], tower.transform)
                if mesh_hit_info.hit:
                    # Save the closest hit mesh
                    if not collision.hit or collision.distance > mesh_hit_info.distance:
                        collision = mesh_hit_info
                    
                    break  # Stop once one mesh collision is detected, the colliding mesh is m

            if mesh_hit_info.hit:
                collision = mesh_hit_info
                cursor_color = rl.ORANGE
                hit_object_name = "Mesh"
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_3d(camera)

        # Draw the tower
        # WARNING: If scale is different than 1.0f,
        # not considered by GetRayCollisionModel()
        rl.draw_model(tower, tower_pos, 1.0, rl.WHITE)

        # Draw the test triangle
        rl.draw_line_3d(ta, tb, rl.PURPLE)
        rl.draw_line_3d(tb, tc, rl.PURPLE)
        rl.draw_line_3d(tc, ta, rl.PURPLE)

        # Draw the test sphere
        rl.draw_sphere_wires(sp, sr, 8, 8, rl.PURPLE)

        # Draw the mesh bbox if we hit it
        if box_hit_info.hit:
            rl.draw_bounding_box(tower_bbox, rl.LIME)

        # If we hit something, draw the cursor at the hit point
        if collision.hit:
            rl.draw_cube(collision.point, 0.3, 0.3, 0.3, cursor_color)
            rl.draw_cube_wires(collision.point, 0.3, 0.3, 0.3, rl.RED)

            normal_end = rl.Vector3(0, 0, 0)
            normal_end.x = collision.point.x + collision.normal.x
            normal_end.y = collision.point.y + collision.normal.y
            normal_end.z = collision.point.z + collision.normal.z

            rl.draw_line_3d(collision.point, normal_end, rl.RED)

        rl.draw_ray(ray, rl.MAROON)

        rl.draw_grid(10, 10.0)

        rl.end_mode_3d()

        # Draw some debug GUI text
        rl.draw_text(f"Hit Object: {hit_object_name}", 10, 50, 10, rl.BLACK)

        if collision.hit:
            ypos = 70

            rl.draw_text(f"Distance: {collision.distance:.2f}", 10, ypos, 10, rl.BLACK)

            rl.draw_text(f"Hit Pos: {collision.point.x:.2f} {collision.point.y:.2f} {collision.point.z:.2f}",
                        10, ypos + 15, 10, rl.BLACK)

            rl.draw_text(f"Hit Norm: {collision.normal.x:.2f} {collision.normal.y:.2f} {collision.normal.z:.2f}",
                        10, ypos + 30, 10, rl.BLACK)

            if tri_hit_info.hit and hit_object_name == "Triangle":
                rl.draw_text(f"Barycenter: {bary.x:.2f} {bary.y:.2f} {bary.z:.2f}",
                            10, ypos + 45, 10, rl.BLACK)

        rl.draw_text("Right click mouse to toggle camera controls", 10, 430, 10, rl.GRAY)

        rl.draw_text("(c) Turret 3D model by Alberto Cano", screen_width - 200, screen_height - 20, 10, rl.GRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.unload_model(tower)      # Unload model
    rl.unload_texture(texture)  # Unload texture

    rl.close_window()           # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
