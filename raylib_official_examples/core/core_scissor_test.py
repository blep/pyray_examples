"""raylib [core] example - Scissor test
Example complexity rating: [★☆☆☆] 1/4
Example originally created with raylib 2.5, last time updated with raylib 3.0
Example contributed by Chris Dill (@MysteriousSpace) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2019-2025 Chris Dill (@MysteriousSpace)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - scissor test")

    scissor_area = rl.Rectangle(0, 0, 300, 300)
    scissor_mode = True

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        if rl.is_key_pressed(rl.KeyboardKey.KEY_S):
            scissor_mode = not scissor_mode

        # Centre the scissor area around the mouse position
        scissor_area.x = rl.get_mouse_x() - scissor_area.width / 2
        scissor_area.y = rl.get_mouse_y() - scissor_area.height / 2
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        if scissor_mode:
            rl.begin_scissor_mode(int(scissor_area.x), int(scissor_area.y), int(scissor_area.width), int(scissor_area.height))

        # Draw full screen rectangle and some text
        # NOTE: Only part defined by scissor area will be rendered
        rl.draw_rectangle(0, 0, rl.get_screen_width(), rl.get_screen_height(), rl.RED)
        rl.draw_text("Move the mouse around to reveal this text!", 190, 200, 20, rl.LIGHTGRAY)

        if scissor_mode:
            rl.end_scissor_mode()

        rl.draw_rectangle_lines_ex(scissor_area, 1, rl.BLACK)
        rl.draw_text("Press S to toggle scissor test", 10, 10, 20, rl.BLACK)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
