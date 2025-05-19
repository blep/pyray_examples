"""raylib [core] example - input virtual controls
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 5.0, last time updated with raylib 5.0
Example create by GreenSnakeLinux (@GreenSnakeLinux),
lighter by oblerion (@oblerion) and 
reviewed by Ramon Santamaria (@raysan5) and
improved by danilwhale (@danilwhale)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2024-2025 oblerion (@oblerion) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math

class PadButton:
    BUTTON_NONE = -1
    BUTTON_UP = 0
    BUTTON_LEFT = 1
    BUTTON_RIGHT = 2
    BUTTON_DOWN = 3
    BUTTON_MAX = 4

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - input virtual controls")

    pad_position = rl.Vector2(100, 350)
    button_radius = 30.0

    button_positions = [
        rl.Vector2(pad_position.x, pad_position.y - button_radius * 1.5),
        rl.Vector2(pad_position.x - button_radius * 1.5, pad_position.y),
        rl.Vector2(pad_position.x + button_radius * 1.5, pad_position.y),
        rl.Vector2(pad_position.x, pad_position.y + button_radius * 1.5)
    ]

    button_labels = [
        "Y",  # Up
        "X",  # Left
        "B",  # Right
        "A"   # Down
    ]

    button_label_colors = [
        rl.YELLOW,  # Up
        rl.BLUE,    # Left
        rl.RED,     # Right
        rl.GREEN    # Down
    ]

    pressed_button = PadButton.BUTTON_NONE
    input_position = rl.Vector2(0, 0)

    player_position = rl.Vector2(float(screen_width) / 2, float(screen_height) / 2)
    player_speed = 75.0

    rl.set_target_fps(60)
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # --------------------------------------------------------------------------
        if rl.get_touch_point_count() > 0:
            # Use touch position
            input_position = rl.get_touch_position(0)
        else:
            # Use mouse position
            input_position = rl.get_mouse_position()

        # Reset pressed button to none
        pressed_button = PadButton.BUTTON_NONE

        # Make sure user is pressing left mouse button if they're from desktop
        if (rl.get_touch_point_count() > 0) or ((rl.get_touch_point_count() == 0) and rl.is_mouse_button_down(rl.MouseButton.MOUSE_BUTTON_LEFT)):
            # Find nearest D-Pad button to the input position
            for i in range(PadButton.BUTTON_MAX):
                dist_x = math.fabs(button_positions[i].x - input_position.x)
                dist_y = math.fabs(button_positions[i].y - input_position.y)

                if (dist_x + dist_y < button_radius):
                    pressed_button = i
                    break
        
        # Move player according to pressed button
        if pressed_button == PadButton.BUTTON_UP:
            player_position.y -= player_speed * rl.get_frame_time()
        elif pressed_button == PadButton.BUTTON_LEFT:
            player_position.x -= player_speed * rl.get_frame_time()
        elif pressed_button == PadButton.BUTTON_RIGHT:
            player_position.x += player_speed * rl.get_frame_time()
        elif pressed_button == PadButton.BUTTON_DOWN:
            player_position.y += player_speed * rl.get_frame_time()

        # --------------------------------------------------------------------------
        # Draw
        # --------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        # Draw world
        rl.draw_circle_v(player_position, 50, rl.MAROON)

        # Draw GUI
        for i in range(PadButton.BUTTON_MAX):
            rl.draw_circle_v(button_positions[i], button_radius, rl.DARKGRAY if i == pressed_button else rl.BLACK)
            rl.draw_text(button_labels[i],
                         int(button_positions[i].x - 7), int(button_positions[i].y - 8),
                         20, button_label_colors[i])

        rl.draw_text("move the player with D-Pad buttons", 10, 10, 20, rl.DARKGRAY)

        rl.end_drawing()
        # --------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
