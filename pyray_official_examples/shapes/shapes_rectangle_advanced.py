"""raylib [shapes] example - Rectangle advanced
Example complexity rating: [★★★★] 4/4
Example originally created with raylib 5.5, last time updated with raylib 5.5
Example contributed by Everton Jr. (@evertonse) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 Everton Jr. (@evertonse) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
import math
THIS_DIR = Path(__file__).resolve().parent

# Draw rectangle with rounded edges and horizontal gradient, with options to choose side of roundness
# NOTE: Adapted from both 'DrawRectangleRounded()' and 'DrawRectangleGradientH()' raylib [rshapes] implementations
def draw_rectangle_rounded_gradient_h(rec, roundness_left, roundness_right, segments, left, right):
    # Neither side is rounded
    if ((roundness_left <= 0.0 and roundness_right <= 0.0) or (rec.width < 1) or (rec.height < 1)):
        rl.draw_rectangle_gradient_ex(rec, left, left, right, right)
        return

    if roundness_left >= 1.0:
        roundness_left = 1.0
    if roundness_right >= 1.0:
        roundness_right = 1.0

    # Calculate corner radius both from right and left
    rec_size = rec.width if rec.width < rec.height else rec.height
    radius_left = (rec_size * roundness_left) / 2
    radius_right = (rec_size * roundness_right) / 2

    if radius_left <= 0.0:
        radius_left = 0.0
    if radius_right <= 0.0:
        radius_right = 0.0

    if radius_right <= 0.0 and radius_left <= 0.0:
        return

    step_length = 90.0 / segments

    # Coordinates of the 12 points adapted from `DrawRectangleRounded`
    """
    Diagram Copied here for reference, original at 'DrawRectangleRounded()' source code

          P0____________________P1
          /|                    |\
         /1|          2         |3\
     P7 /__|____________________|__\ P2
       |   |P8                P9|   |
       | 8 |          9         | 4 |
       | __|____________________|__ |
     P6 \  |P11              P10|  / P3
         \7|          6         |5/
          \|____________________|/
          P5                    P4
    """

    # Points array
    point = [
        # P0, P1, P2
        rl.Vector2(rec.x + radius_left, rec.y), 
        rl.Vector2(rec.x + rec.width - radius_right, rec.y), 
        rl.Vector2(rec.x + rec.width, rec.y + radius_right),
        # P3, P4
        rl.Vector2(rec.x + rec.width, rec.y + rec.height - radius_right), 
        rl.Vector2(rec.x + rec.width - radius_right, rec.y + rec.height),
        # P5, P6, P7
        rl.Vector2(rec.x + radius_left, rec.y + rec.height),
        rl.Vector2(rec.x, rec.y + rec.height - radius_left),
        rl.Vector2(rec.x, rec.y + radius_left),
        # P8, P9
        rl.Vector2(rec.x + radius_left, rec.y + radius_left),
        rl.Vector2(rec.x + rec.width - radius_right, rec.y + radius_right),
        # P10, P11
        rl.Vector2(rec.x + rec.width - radius_right, rec.y + rec.height - radius_right),
        rl.Vector2(rec.x + radius_left, rec.y + rec.height - radius_left)
    ]

    centers = [point[8], point[9], point[10], point[11]]
    angles = [180.0, 270.0, 0.0, 90.0]

    # Here we use the 'Diagram' to guide ourselves to which point receives what color.
    # By choosing the color correctly associated with a point the gradient effect 
    # will naturally come from OpenGL interpolation.
    # But instead of Quads, we use triangles.

    rl.rl_begin(rl.RL_TRIANGLES)

    # Draw all of the 4 corners: [1] Upper Left Corner, [3] Upper Right Corner, [5] Lower Right Corner, [7] Lower Left Corner
    for k in range(4):
        if k == 0:  # [1] Upper Left Corner
            color = left
            radius = radius_left
        elif k == 1:  # [3] Upper Right Corner
            color = right
            radius = radius_right
        elif k == 2:  # [5] Lower Right Corner
            color = right
            radius = radius_right
        else:  # k == 3, [7] Lower Left Corner 
            color = left
            radius = radius_left
        
        angle = angles[k]
        center = centers[k]
        
        for i in range(segments):
            rl.rl_color4ub(color.r, color.g, color.b, color.a)
            rl.rl_vertex2f(center.x, center.y)
            rl.rl_vertex2f(
                center.x + math.cos(math.radians(angle + step_length)) * radius,
                center.y + math.sin(math.radians(angle + step_length)) * radius
            )
            rl.rl_vertex2f(
                center.x + math.cos(math.radians(angle)) * radius,
                center.y + math.sin(math.radians(angle)) * radius
            )
            angle += step_length

    # [2] Upper Rectangle
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[0].x, point[0].y)
    rl.rl_vertex2f(point[8].x, point[8].y)
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[9].x, point[9].y)

    rl.rl_vertex2f(point[1].x, point[1].y)
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[0].x, point[0].y)
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[9].x, point[9].y)

    # [4] Right Rectangle
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[9].x, point[9].y)
    rl.rl_vertex2f(point[10].x, point[10].y)
    rl.rl_vertex2f(point[3].x, point[3].y)

    rl.rl_vertex2f(point[2].x, point[2].y)
    rl.rl_vertex2f(point[9].x, point[9].y)
    rl.rl_vertex2f(point[3].x, point[3].y)

    # [6] Bottom Rectangle
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[11].x, point[11].y)
    rl.rl_vertex2f(point[5].x, point[5].y)
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[4].x, point[4].y)

    rl.rl_vertex2f(point[10].x, point[10].y)
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[11].x, point[11].y)
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[4].x, point[4].y)

    # [8] Left Rectangle
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[7].x, point[7].y)
    rl.rl_vertex2f(point[6].x, point[6].y)
    rl.rl_vertex2f(point[11].x, point[11].y)

    rl.rl_vertex2f(point[8].x, point[8].y)
    rl.rl_vertex2f(point[7].x, point[7].y)
    rl.rl_vertex2f(point[11].x, point[11].y)

    # [9] Middle Rectangle
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[8].x, point[8].y)
    rl.rl_vertex2f(point[11].x, point[11].y)
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[10].x, point[10].y)

    rl.rl_vertex2f(point[9].x, point[9].y)
    rl.rl_color4ub(left.r, left.g, left.b, left.a)
    rl.rl_vertex2f(point[8].x, point[8].y)
    rl.rl_color4ub(right.r, right.g, right.b, right.a)
    rl.rl_vertex2f(point[10].x, point[10].y)

    rl.rl_end()

def main():
    # Initialization
    #--------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450
    
    rl.init_window(screen_width, screen_height, "raylib [shapes] example - rectangle advanced")
    
    rl.set_target_fps(60)               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update rectangle bounds
        #----------------------------------------------------------------------------------
        width = rl.get_screen_width()/2.0
        height = rl.get_screen_height()/6.0
        rec = rl.Rectangle(
            rl.get_screen_width()/2.0 - width/2,
            rl.get_screen_height()/2.0 - 5*(height/2),
            width, height
        )
        #--------------------------------------------------------------------------------------

        # Draw
        #----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Draw All Rectangles with different roundess for each side and different gradients
        draw_rectangle_rounded_gradient_h(rec, 0.8, 0.8, 36, rl.BLUE, rl.RED)

        rec.y += rec.height + 1
        draw_rectangle_rounded_gradient_h(rec, 0.5, 1.0, 36, rl.RED, rl.PINK)

        rec.y += rec.height + 1
        draw_rectangle_rounded_gradient_h(rec, 1.0, 0.5, 36, rl.RED, rl.BLUE)

        rec.y += rec.height + 1
        draw_rectangle_rounded_gradient_h(rec, 0.0, 1.0, 36, rl.BLUE, rl.BLACK)

        rec.y += rec.height + 1
        draw_rectangle_rounded_gradient_h(rec, 1.0, 0.0, 36, rl.BLUE, rl.PINK)
        
        rl.end_drawing()
        #--------------------------------------------------------------------------------------

    # De-Initialization
    #--------------------------------------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()