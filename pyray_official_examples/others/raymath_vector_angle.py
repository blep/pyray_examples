"""raylib [shapes] example - Vector Angle
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.0, last time updated with raylib 4.6
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
from pathlib import Path
THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [math] example - vector angle")

    v0 = rl.Vector2(screen_width/2, screen_height/2)
    v1 = rl.vector2_add(v0, rl.Vector2(100.0, 80.0))
    v2 = rl.Vector2(0, 0)  # Updated with mouse position
    
    angle = 0.0  # Angle in degrees
    angle_mode = 0  # 0-Vector2Angle(), 1-Vector2LineAngle()

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        start_angle = 0.0

        if angle_mode == 0:
            start_angle = -rl.vector2_line_angle(v0, v1) * rl.RAD2DEG
        elif angle_mode == 1:
            start_angle = 0.0

        v2 = rl.get_mouse_position()

        if rl.is_key_pressed(rl.KEY_SPACE):
            angle_mode = 0 if angle_mode == 1 else 1
        
        if angle_mode == 0 and rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
            v1 = rl.get_mouse_position()

        if angle_mode == 0:
            # Calculate angle between two vectors, considering a common origin (v0)
            v1_normal = rl.vector2_normalize(rl.vector2_subtract(v1, v0))
            v2_normal = rl.vector2_normalize(rl.vector2_subtract(v2, v0))

            angle = rl.vector2_angle(v1_normal, v2_normal) * rl.RAD2DEG
        elif angle_mode == 1:
            # Calculate angle defined by a two vectors line, in reference to horizontal line
            angle = rl.vector2_line_angle(v0, v2) * rl.RAD2DEG

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        
        if angle_mode == 0:
            rl.draw_text("MODE 0: Angle between V1 and V2", 10, 10, 20, rl.BLACK)
            rl.draw_text("Right Click to Move V2", 10, 30, 20, rl.DARKGRAY)
            
            rl.draw_line_ex(v0, v1, 2.0, rl.BLACK)
            rl.draw_line_ex(v0, v2, 2.0, rl.RED)

            rl.draw_circle_sector(v0, 40.0, start_angle, start_angle + angle, 32, rl.fade(rl.GREEN, 0.6))
        elif angle_mode == 1:
            rl.draw_text("MODE 1: Angle formed by line V1 to V2", 10, 10, 20, rl.BLACK)
            
            rl.draw_line(0, screen_height//2, screen_width, screen_height//2, rl.LIGHTGRAY)
            rl.draw_line_ex(v0, v2, 2.0, rl.RED)

            rl.draw_circle_sector(v0, 40.0, start_angle, start_angle - angle, 32, rl.fade(rl.GREEN, 0.6))
        
        rl.draw_text("v0", int(v0.x), int(v0.y), 10, rl.DARKGRAY)

        # Adjust the position of the v1 text if it would overlap v0
        if angle_mode == 0:
            # Draw v1 label with offset to avoid overlapping
            text_offset_x = 10 if v1.x > v0.x else -20
            text_offset_y = -10 if v1.y < v0.y else 10
            rl.draw_text("v1", int(v1.x + text_offset_x), int(v1.y + text_offset_y), 10, rl.DARKGRAY)

        # Draw v2 label with offset to avoid overlapping
        text_offset_x = 10 if v2.x > v0.x else -20
        text_offset_y = -10 if v2.y < v0.y else 10
        rl.draw_text("v2", int(v2.x + text_offset_x), int(v2.y + text_offset_y), 10, rl.RED)

        # Draw the actual angle value
        rl.draw_text(f"angle: {angle:.2f} degrees", 10, screen_height - 30, 20, rl.DARKGRAY)
        rl.draw_text("Press SPACE to change MODE", screen_width - 230, screen_height - 30, 20, rl.DARKGRAY)

        rl.end_drawing()

    # De-Initialization
    rl.close_window()

if __name__ == "__main__":
    main()
