"""raylib [shapes] example - following eyes
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import math
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - following eyes")

    sclera_left_position = rl.Vector2(rl.get_screen_width()/2.0 - 100.0, rl.get_screen_height()/2.0)
    sclera_right_position = rl.Vector2(rl.get_screen_width()/2.0 + 100.0, rl.get_screen_height()/2.0)
    sclera_radius = 80

    iris_left_position = rl.Vector2(rl.get_screen_width()/2.0 - 100.0, rl.get_screen_height()/2.0)
    iris_right_position = rl.Vector2(rl.get_screen_width()/2.0 + 100.0, rl.get_screen_height()/2.0)
    iris_radius = 24

    angle = 0.0
    dx = 0.0
    dy = 0.0
    dxx = 0.0
    dyy = 0.0

    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        iris_left_position = rl.get_mouse_position()
        iris_right_position = rl.get_mouse_position()

        # Check not inside the left eye sclera
        if not rl.check_collision_point_circle(iris_left_position, sclera_left_position, sclera_radius - iris_radius):
            dx = iris_left_position.x - sclera_left_position.x
            dy = iris_left_position.y - sclera_left_position.y

            angle = math.atan2(dy, dx)

            dxx = (sclera_radius - iris_radius) * math.cos(angle)
            dyy = (sclera_radius - iris_radius) * math.sin(angle)

            iris_left_position.x = sclera_left_position.x + dxx
            iris_left_position.y = sclera_left_position.y + dyy

        # Check not inside the right eye sclera
        if not rl.check_collision_point_circle(iris_right_position, sclera_right_position, sclera_radius - iris_radius):
            dx = iris_right_position.x - sclera_right_position.x
            dy = iris_right_position.y - sclera_right_position.y

            angle = math.atan2(dy, dx)

            dxx = (sclera_radius - iris_radius) * math.cos(angle)
            dyy = (sclera_radius - iris_radius) * math.sin(angle)

            iris_right_position.x = sclera_right_position.x + dxx
            iris_right_position.y = sclera_right_position.y + dyy
        #----------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_circle_v(sclera_left_position, sclera_radius, rl.LIGHTGRAY)
        rl.draw_circle_v(iris_left_position, iris_radius, rl.BROWN)
        rl.draw_circle_v(iris_left_position, 10, rl.BLACK)

        rl.draw_circle_v(sclera_right_position, sclera_radius, rl.LIGHTGRAY)
        rl.draw_circle_v(iris_right_position, iris_radius, rl.DARKGREEN)
        rl.draw_circle_v(iris_right_position, 10, rl.BLACK)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #----------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()