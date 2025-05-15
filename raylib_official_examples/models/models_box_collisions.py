"""raylib [models] example - Detect basic 3d collisions (box vs sphere vs box)
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 1.3, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path

# Get the directory of the current script
THIS_DIR = Path(__file__).resolve().parent

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [models] example - box collisions")

    # Define the camera to look into our 3d world
    camera = rl.Camera3D()
    camera.position = rl.Vector3(0.0, 10.0, 10.0)
    camera.target = rl.Vector3(0.0, 0.0, 0.0)
    camera.up = rl.Vector3(0.0, 1.0, 0.0)
    camera.fovy = 45.0
    camera.projection = rl.CAMERA_PERSPECTIVE

    player_position = rl.Vector3(0.0, 1.0, 2.0)
    player_size = rl.Vector3(1.0, 2.0, 1.0)
    player_color = rl.GREEN

    enemy_box_pos = rl.Vector3(-4.0, 1.0, 0.0)
    enemy_box_size = rl.Vector3(2.0, 2.0, 2.0)

    enemy_sphere_pos = rl.Vector3(4.0, 0.0, 0.0)
    enemy_sphere_size = 1.5

    collision = False

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():   # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        # Move player
        if rl.is_key_down(rl.KEY_RIGHT): player_position.x += 0.2
        elif rl.is_key_down(rl.KEY_LEFT): player_position.x -= 0.2
        elif rl.is_key_down(rl.KEY_DOWN): player_position.z += 0.2
        elif rl.is_key_down(rl.KEY_UP): player_position.z -= 0.2

        collision = False

        # Check collisions player vs enemy-box
        player_bbox = rl.BoundingBox(
            rl.Vector3(player_position.x - player_size.x/2,
                      player_position.y - player_size.y/2,
                      player_position.z - player_size.z/2),
            rl.Vector3(player_position.x + player_size.x/2,
                      player_position.y + player_size.y/2,
                      player_position.z + player_size.z/2)
        )
        
        enemy_bbox = rl.BoundingBox(
            rl.Vector3(enemy_box_pos.x - enemy_box_size.x/2,
                      enemy_box_pos.y - enemy_box_size.y/2,
                      enemy_box_pos.z - enemy_box_size.z/2),
            rl.Vector3(enemy_box_pos.x + enemy_box_size.x/2,
                      enemy_box_pos.y + enemy_box_size.y/2,
                      enemy_box_pos.z + enemy_box_size.z/2)
        )
        
        if rl.check_collision_boxes(player_bbox, enemy_bbox):
            collision = True

        # Check collisions player vs enemy-sphere
        if rl.check_collision_box_sphere(player_bbox, enemy_sphere_pos, enemy_sphere_size):
            collision = True

        player_color = rl.RED if collision else rl.GREEN
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        
        rl.clear_background(rl.RAYWHITE)
        
        rl.begin_mode_3d(camera)
        
        # Draw enemy-box
        rl.draw_cube(enemy_box_pos, enemy_box_size.x, enemy_box_size.y, enemy_box_size.z, rl.GRAY)
        rl.draw_cube_wires(enemy_box_pos, enemy_box_size.x, enemy_box_size.y, enemy_box_size.z, rl.DARKGRAY)
        
        # Draw enemy-sphere
        rl.draw_sphere(enemy_sphere_pos, enemy_sphere_size, rl.GRAY)
        rl.draw_sphere_wires(enemy_sphere_pos, enemy_sphere_size, 16, 16, rl.DARKGRAY)
        
        # Draw player
        rl.draw_cube_v(player_position, player_size, player_color)
        
        rl.draw_grid(10, 1.0)        # Draw a grid
        
        rl.end_mode_3d()
        
        rl.draw_text("Move player with arrow keys to collide", 220, 40, 20, rl.GRAY)
        
        rl.draw_fps(10, 10)
        
        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------
