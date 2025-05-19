"""raylib [core] example - 2d camera mouse zoom
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 4.2, last time updated with raylib 4.2
Example contributed by Jeffery Myers (@JeffM2501) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2022-2025 Jeffery Myers (@JeffM2501)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

def main():
    # Initialization
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 2d camera mouse zoom")

    camera = rl.Camera2D()
    camera.offset = rl.Vector2(0, 0)
    camera.target = rl.Vector2(0, 0)
    camera.rotation = 0.0
    camera.zoom = 1.0

    zoom_mode = 0  # 0-Mouse Wheel, 1-Mouse Move

    rl.set_target_fps(60)

    # Main game loop
    while not rl.window_should_close():
        # Update
        # ----------------------------------------------------------------------------------
        if rl.is_key_pressed(rl.KEY_ONE):
            zoom_mode = 0
        elif rl.is_key_pressed(rl.KEY_TWO):
            zoom_mode = 1
        
        # Translate based on mouse left click
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            delta = rl.get_mouse_delta()
            delta = rl.vector2_scale(delta, -1.0 / camera.zoom)
            camera.target = rl.vector2_add(camera.target, delta)

        if zoom_mode == 0:
            # Zoom based on mouse wheel
            wheel = rl.get_mouse_wheel_move()
            if wheel != 0:
                # Get the world point that is under the mouse
                mouse_world_pos = rl.get_screen_to_world_2d(rl.get_mouse_position(), camera)

                # Set the offset to where the mouse is
                camera.offset = rl.get_mouse_position()

                # Set the target to match, so that the camera maps the world space point 
                # under the cursor to the screen space point under the cursor at any zoom
                camera.target = mouse_world_pos

                # Zoom increment (uses log scaling for consistent zoom speed)
                scale = 0.2 * wheel
                # Clamp zoom value
                camera.zoom = rl.clamp(math.exp(math.log(camera.zoom) + scale), 0.125, 64.0)
        else: # zoom_mode == 1
            # Zoom based on mouse right click and move
            if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
                # Get the world point that is under the mouse
                mouse_world_pos = rl.get_screen_to_world_2d(rl.get_mouse_position(), camera)

                # Set the offset to where the mouse is
                camera.offset = rl.get_mouse_position()

                # Set the target to match
                camera.target = mouse_world_pos
            
            if rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
                # Zoom increment (uses log scaling for consistent zoom speed)
                delta_x = rl.get_mouse_delta().x
                scale = 0.005 * delta_x
                # Clamp zoom value
                camera.zoom = rl.clamp(math.exp(math.log(camera.zoom) + scale), 0.125, 64.0)
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        rl.begin_mode_2d(camera)

        # Draw the 3d grid, rotated 90 degrees and centered around 0,0        # just so we have something in the XY plane
        rl.rl_push_matrix()
        rl.rl_translatef(0, 25 * 50, 0)
        rl.rl_rotatef(90, 1, 0, 0)
        rl.draw_grid(100, 50)
        rl.rl_pop_matrix()

        # Draw a reference circle
        rl.draw_circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50, rl.MAROON)
            
        rl.end_mode_2d()
        
        # Draw mouse reference coordinates and circle
        mouse_pos_screen = rl.get_mouse_position()
        rl.draw_circle_v(mouse_pos_screen, 4, rl.DARKGRAY)
        
        mouse_text = f"[{int(mouse_pos_screen.x)}, {int(mouse_pos_screen.y)}]"
        text_pos = rl.vector2_add(mouse_pos_screen, rl.Vector2(-44, -24)) # Offset text slightly
        rl.draw_text_ex(rl.get_font_default(), mouse_text, text_pos, 20, 2, rl.BLACK)

        rl.draw_text("[1][2] Select mouse zoom mode (Wheel or Move)", 20, 20, 20, rl.DARKGRAY)
        if zoom_mode == 0:
            rl.draw_text("Mouse left button drag to move, mouse wheel to zoom", 20, 50, 20, rl.DARKGRAY)
        else:
            rl.draw_text("Mouse left button drag to move, mouse right button press and move to zoom", 20, 50, 20, rl.DARKGRAY)
    
        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
