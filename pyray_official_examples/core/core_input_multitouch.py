"""raylib [core] example - Input multitouch
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 2.1, last time updated with raylib 2.5
Example contributed by Berni (@Berni8k) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Berni (@Berni8k) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

MAX_TOUCH_POINTS = 10

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - input multitouch")

    touch_positions = [rl.Vector2(0, 0) for _ in range(MAX_TOUCH_POINTS)]

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # ---------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        # Get the touch point count ( how many fingers are touching the screen )
        t_count = rl.get_touch_point_count()
        # Clamp touch points available ( set the maximum touch points allowed )
        if t_count > MAX_TOUCH_POINTS:
            t_count = MAX_TOUCH_POINTS
        # Get touch points positions
        for i in range(t_count):
            touch_positions[i] = rl.get_touch_position(i)
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        for i in range(t_count):
            # Make sure point is not (0, 0) as this means there is no touch for it
            # In pyray, (0,0) can be a valid touch if it's at the top-left corner.
            # The original C code might rely on (0,0) being an uninitialized/default value for non-active touches.
            # pyray's get_touch_position might return valid coordinates even if a touch just ended.
            # A more robust check might involve checking if a touch point is active, if such API exists in pyray,
            # or rely on t_count being accurate.
            # For this direct port, we'll keep the (0,0) check, but it might behave differently.
            if not (touch_positions[i].x == 0 and touch_positions[i].y == 0):
                # Draw circle and touch index number
                rl.draw_circle_v(touch_positions[i], 34, rl.ORANGE)
                rl.draw_text(f"{i}", int(touch_positions[i].x) - 10, int(touch_positions[i].y) - 70, 40, rl.BLACK)

        rl.draw_text("touch the screen at multiple locations to get multiple balls", 10, 10, 20, rl.DARKGRAY)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
