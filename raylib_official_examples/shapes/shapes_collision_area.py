"""raylib [shapes] example - collision area
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    #---------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [shapes] example - collision area")

    # Box A: Moving box
    box_a = rl.Rectangle(10, rl.get_screen_height()/2.0 - 50, 200, 100)
    box_a_speed_x = 4

    # Box B: Mouse moved box
    box_b = rl.Rectangle(rl.get_screen_width()/2.0 - 30, rl.get_screen_height()/2.0 - 30, 60, 60)

    box_collision = rl.Rectangle(0, 0, 0, 0)  # Collision rectangle

    screen_upper_limit = 40      # Top menu limits

    pause = False             # Movement pause
    collision = False         # Collision detection

    rl.set_target_fps(60)     # Set our game to run at 60 frames-per-second
    #----------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():    # Detect window close button or ESC key
        # Update
        #-----------------------------------------------------
        # Move box if not paused
        if not pause:
            box_a.x += box_a_speed_x

        # Bounce box on x screen limits
        if ((box_a.x + box_a.width) >= rl.get_screen_width()) or (box_a.x <= 0): 
            box_a_speed_x *= -1

        # Update player-controlled-box (box02)
        box_b.x = rl.get_mouse_x() - box_b.width/2
        box_b.y = rl.get_mouse_y() - box_b.height/2

        # Make sure Box B does not go out of move area limits
        if (box_b.x + box_b.width) >= rl.get_screen_width():
            box_b.x = rl.get_screen_width() - box_b.width
        elif box_b.x <= 0:
            box_b.x = 0

        if (box_b.y + box_b.height) >= rl.get_screen_height():
            box_b.y = rl.get_screen_height() - box_b.height
        elif box_b.y <= screen_upper_limit:
            box_b.y = screen_upper_limit

        # Check boxes collision
        collision = rl.check_collision_recs(box_a, box_b)

        # Get collision rectangle (only on collision)
        if collision:
            box_collision = rl.get_collision_rec(box_a, box_b)

        # Pause Box A movement
        if rl.is_key_pressed(rl.KEY_SPACE):
            pause = not pause
        #-----------------------------------------------------

        # Draw
        #-----------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle(0, 0, screen_width, screen_upper_limit, rl.RED if collision else rl.BLACK)

        rl.draw_rectangle_rec(box_a, rl.GOLD)
        rl.draw_rectangle_rec(box_b, rl.BLUE)

        if collision:
            # Draw collision area
            rl.draw_rectangle_rec(box_collision, rl.LIME)

            # Draw collision message
            rl.draw_text("COLLISION!", rl.get_screen_width()//2 - rl.measure_text("COLLISION!", 20)//2, screen_upper_limit//2 - 10, 20, rl.BLACK)

            # Draw collision area
            collision_area_text = f"Collision Area: {int(box_collision.width*box_collision.height)}"
            rl.draw_text(collision_area_text, rl.get_screen_width()//2 - 100, screen_upper_limit + 10, 20, rl.BLACK)

        # Draw help instructions
        rl.draw_text("Press SPACE to PAUSE/RESUME", 20, screen_height - 35, 20, rl.LIGHTGRAY)

        rl.draw_fps(10, 10)

        rl.end_drawing()
        #-----------------------------------------------------

    # De-Initialization
    #---------------------------------------------------------
    rl.close_window()        # Close window and OpenGL context
    #----------------------------------------------------------

if __name__ == "__main__":
    main()