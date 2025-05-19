"""raylib [core] example - window flags
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 3.5, last time updated with raylib 3.5
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2020-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

def main():
    screen_width = 800
    screen_height = 450

    # rl.set_config_flags(rl.FLAG_VSYNC_HINT | rl.FLAG_MSAA_4X_HINT | rl.FLAG_WINDOW_HIGHDPI)
    rl.init_window(screen_width, screen_height, "raylib [core] example - window flags")

    ball_position = rl.Vector2(rl.get_screen_width() / 2.0, rl.get_screen_height() / 2.0)
    ball_speed = rl.Vector2(5.0, 4.0)
    ball_radius = 20.0

    frames_counter = 0

    rl.set_target_fps(60)

    while not rl.window_should_close():
        if rl.is_key_pressed(rl.KEY_F):
            rl.toggle_fullscreen()

        if rl.is_key_pressed(rl.KEY_R):
            if rl.is_window_state(rl.FLAG_WINDOW_RESIZABLE):
                rl.clear_window_state(rl.FLAG_WINDOW_RESIZABLE)
            else:
                rl.set_window_state(rl.FLAG_WINDOW_RESIZABLE)

        if rl.is_key_pressed(rl.KEY_D):
            if rl.is_window_state(rl.FLAG_WINDOW_UNDECORATED):
                rl.clear_window_state(rl.FLAG_WINDOW_UNDECORATED)
            else:
                rl.set_window_state(rl.FLAG_WINDOW_UNDECORATED)

        if rl.is_key_pressed(rl.KEY_H):
            if not rl.is_window_state(rl.FLAG_WINDOW_HIDDEN):
                rl.set_window_state(rl.FLAG_WINDOW_HIDDEN)
            frames_counter = 0

        if rl.is_window_state(rl.FLAG_WINDOW_HIDDEN):
            frames_counter += 1
            if frames_counter >= 240:
                rl.clear_window_state(rl.FLAG_WINDOW_HIDDEN)

        if rl.is_key_pressed(rl.KEY_N):
            if not rl.is_window_state(rl.FLAG_WINDOW_MINIMIZED):
                rl.minimize_window()
            frames_counter = 0
            
        if rl.is_window_state(rl.FLAG_WINDOW_MINIMIZED):
            frames_counter += 1
            if frames_counter >= 240:
                rl.restore_window()
                frames_counter = 0

        if rl.is_key_pressed(rl.KEY_M):
            if rl.is_window_state(rl.FLAG_WINDOW_MAXIMIZED):
                rl.restore_window()
            else:
                rl.maximize_window()

        if rl.is_key_pressed(rl.KEY_U):
            if rl.is_window_state(rl.FLAG_WINDOW_UNFOCUSED):
                rl.clear_window_state(rl.FLAG_WINDOW_UNFOCUSED)
            else:
                rl.set_window_state(rl.FLAG_WINDOW_UNFOCUSED)

        if rl.is_key_pressed(rl.KEY_T):
            if rl.is_window_state(rl.FLAG_WINDOW_TOPMOST):
                rl.clear_window_state(rl.FLAG_WINDOW_TOPMOST)
            else:
                rl.set_window_state(rl.FLAG_WINDOW_TOPMOST)

        if rl.is_key_pressed(rl.KEY_A):
            if rl.is_window_state(rl.FLAG_WINDOW_ALWAYS_RUN):
                rl.clear_window_state(rl.FLAG_WINDOW_ALWAYS_RUN)
            else:
                rl.set_window_state(rl.FLAG_WINDOW_ALWAYS_RUN)

        if rl.is_key_pressed(rl.KEY_V):
            if rl.is_window_state(rl.FLAG_VSYNC_HINT):
                rl.clear_window_state(rl.FLAG_VSYNC_HINT)
            else:
                rl.set_window_state(rl.FLAG_VSYNC_HINT)
        
        if rl.is_key_pressed(rl.KEY_B):
            rl.toggle_borderless_windowed()

        ball_position.x += ball_speed.x
        ball_position.y += ball_speed.y
        if (ball_position.x >= (rl.get_screen_width() - ball_radius)) or (ball_position.x <= ball_radius):
            ball_speed.x *= -1.0
        if (ball_position.y >= (rl.get_screen_height() - ball_radius)) or (ball_position.y <= ball_radius):
            ball_speed.y *= -1.0

        rl.begin_drawing()
        if rl.is_window_state(rl.FLAG_WINDOW_TRANSPARENT):
            rl.clear_background(rl.BLANK)
        else:
            rl.clear_background(rl.RAYWHITE)

        rl.draw_circle_v(ball_position, ball_radius, rl.MAROON)
        rl.draw_rectangle_lines_ex(rl.Rectangle(0, 0, float(rl.get_screen_width()), float(rl.get_screen_height())), 4, rl.RAYWHITE)
        rl.draw_circle_v(rl.get_mouse_position(), 10, rl.DARKBLUE)
        rl.draw_fps(10, 10)
        rl.draw_text(f"Screen Size: [{rl.get_screen_width()}, {rl.get_screen_height()}]", 10, 40, 10, rl.GREEN)

        rl.draw_text("Following flags can be set after window creation:", 10, 60, 10, rl.GRAY)
        if rl.is_window_state(rl.FLAG_FULLSCREEN_MODE): rl.draw_text("[F] FLAG_FULLSCREEN_MODE: on", 10, 80, 10, rl.LIME)
        else: rl.draw_text("[F] FLAG_FULLSCREEN_MODE: off", 10, 80, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_RESIZABLE): rl.draw_text("[R] FLAG_WINDOW_RESIZABLE: on", 10, 100, 10, rl.LIME)
        else: rl.draw_text("[R] FLAG_WINDOW_RESIZABLE: off", 10, 100, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_UNDECORATED): rl.draw_text("[D] FLAG_WINDOW_UNDECORATED: on", 10, 120, 10, rl.LIME)
        else: rl.draw_text("[D] FLAG_WINDOW_UNDECORATED: off", 10, 120, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_HIDDEN): rl.draw_text("[H] FLAG_WINDOW_HIDDEN: on", 10, 140, 10, rl.LIME)
        else: rl.draw_text("[H] FLAG_WINDOW_HIDDEN: off (hides for 3 seconds)", 10, 140, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_MINIMIZED): rl.draw_text("[N] FLAG_WINDOW_MINIMIZED: on", 10, 160, 10, rl.LIME)
        else: rl.draw_text("[N] FLAG_WINDOW_MINIMIZED: off (restores after 3 seconds)", 10, 160, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_MAXIMIZED): rl.draw_text("[M] FLAG_WINDOW_MAXIMIZED: on", 10, 180, 10, rl.LIME)
        else: rl.draw_text("[M] FLAG_WINDOW_MAXIMIZED: off", 10, 180, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_UNFOCUSED): rl.draw_text("[U] FLAG_WINDOW_UNFOCUSED: on", 10, 200, 10, rl.LIME) # Changed G to U for consistency
        else: rl.draw_text("[U] FLAG_WINDOW_UNFOCUSED: off", 10, 200, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_TOPMOST): rl.draw_text("[T] FLAG_WINDOW_TOPMOST: on", 10, 220, 10, rl.LIME)
        else: rl.draw_text("[T] FLAG_WINDOW_TOPMOST: off", 10, 220, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_ALWAYS_RUN): rl.draw_text("[A] FLAG_WINDOW_ALWAYS_RUN: on", 10, 240, 10, rl.LIME)
        else: rl.draw_text("[A] FLAG_WINDOW_ALWAYS_RUN: off", 10, 240, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_VSYNC_HINT): rl.draw_text("[V] FLAG_VSYNC_HINT: on", 10, 260, 10, rl.LIME)
        else: rl.draw_text("[V] FLAG_VSYNC_HINT: off", 10, 260, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_BORDERLESS_WINDOWED_MODE): rl.draw_text("[B] FLAG_BORDERLESS_WINDOWED_MODE: on", 10, 280, 10, rl.LIME)
        else: rl.draw_text("[B] FLAG_BORDERLESS_WINDOWED_MODE: off", 10, 280, 10, rl.MAROON)

        rl.draw_text("Following flags can only be set before window creation:", 10, 320, 10, rl.GRAY)
        # Note: In pyray, these flags are typically set with rl.set_config_flags() before rl.init_window()
        # Checking them with rl.is_window_state() after window creation might not reflect the initial config state accurately for all flags.
        # However, some flags like HIGHDPI might be detectable. For this example, we mirror the C version's intent.
        if rl.is_window_state(rl.FLAG_WINDOW_HIGHDPI): rl.draw_text("FLAG_WINDOW_HIGHDPI: on", 10, 340, 10, rl.LIME)
        else: rl.draw_text("FLAG_WINDOW_HIGHDPI: off", 10, 340, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_WINDOW_TRANSPARENT): rl.draw_text("FLAG_WINDOW_TRANSPARENT: on", 10, 360, 10, rl.LIME)
        else: rl.draw_text("FLAG_WINDOW_TRANSPARENT: off", 10, 360, 10, rl.MAROON)
        if rl.is_window_state(rl.FLAG_MSAA_4X_HINT): rl.draw_text("FLAG_MSAA_4X_HINT: on", 10, 380, 10, rl.LIME)
        else: rl.draw_text("FLAG_MSAA_4X_HINT: off", 10, 380, 10, rl.MAROON)

        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
