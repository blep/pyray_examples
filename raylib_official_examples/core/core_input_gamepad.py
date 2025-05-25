"""raylib [core] example - Gamepad input
Example complexity rating: [★☆☆☆] 1/4
NOTE: This example requires a Gamepad connected to the system
      raylib is configured to work with the following gamepads:
             - Xbox 360 Controller (Xbox 360, Xbox One)
             - PLAYSTATION(R)3 Controller
      Check raylib.h for buttons configuration
Example originally created with raylib 1.1, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2013-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""
from pathlib import Path

import pyray as rl

# NOTE: Gamepad name ID depends on drivers and OS
XBOX_ALIAS_1 = "xbox"
XBOX_ALIAS_2 = "x-box"
PS_ALIAS = "playstation"

THIS_DIR = Path(__file__).resolve().parent

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.set_config_flags(rl.ConfigFlags.FLAG_MSAA_4X_HINT)  # Set MSAA 4X hint before windows creation

    rl.init_window(screen_width, screen_height, "raylib [core] example - gamepad input")

    # NOTE: Textures MUST be loaded after Window initialization (OpenGL context is required)
    tex_ps3_pad = rl.load_texture(str(THIS_DIR/"resources/ps3.png"))
    tex_xbox_pad = rl.load_texture(str(THIS_DIR/"resources/xbox.png"))

    # Set axis deadzones
    left_stick_deadzone_x = 0.1
    left_stick_deadzone_y = 0.1
    right_stick_deadzone_x = 0.1
    right_stick_deadzone_y = 0.1
    left_trigger_deadzone = -0.9
    right_trigger_deadzone = -0.9
    
    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    gamepad = 0  # which gamepad to display

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        # ...
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        if rl.is_key_pressed(rl.KeyboardKey.KEY_LEFT) and gamepad > 0:
            gamepad -= 1
        if rl.is_key_pressed(rl.KeyboardKey.KEY_RIGHT):
            gamepad += 1
            # Check if next gamepad is available, if not, cycle back to 0 or last available
            # This part is a bit tricky as we don't know the max number of connected gamepads easily
            # For simplicity, let's assume we just increment and rely on IsGamepadAvailable
            # A more robust solution would involve checking available gamepads.

        if rl.is_gamepad_available(gamepad):
            gamepad_name = rl.get_gamepad_name(gamepad)
            if gamepad_name: # Check if gamepad_name is not None
                 rl.draw_text(f"GP{gamepad}: {gamepad_name}", 10, 10, 10, rl.BLACK)
            else:
                 rl.draw_text(f"GP{gamepad}: UNKNOWN", 10, 10, 10, rl.BLACK)


            # Get axis values
            left_stick_x = rl.get_gamepad_axis_movement(gamepad, rl.GamepadAxis.GAMEPAD_AXIS_LEFT_X)
            left_stick_y = rl.get_gamepad_axis_movement(gamepad, rl.GamepadAxis.GAMEPAD_AXIS_LEFT_Y)
            right_stick_x = rl.get_gamepad_axis_movement(gamepad, rl.GamepadAxis.GAMEPAD_AXIS_RIGHT_X)
            right_stick_y = rl.get_gamepad_axis_movement(gamepad, rl.GamepadAxis.GAMEPAD_AXIS_RIGHT_Y)
            left_trigger = rl.get_gamepad_axis_movement(gamepad, rl.GamepadAxis.GAMEPAD_AXIS_LEFT_TRIGGER)
            right_trigger = rl.get_gamepad_axis_movement(gamepad, rl.GamepadAxis.GAMEPAD_AXIS_RIGHT_TRIGGER)

            # Calculate deadzones
            if -left_stick_deadzone_x < left_stick_x < left_stick_deadzone_x:
                left_stick_x = 0.0
            if -left_stick_deadzone_y < left_stick_y < left_stick_deadzone_y:
                left_stick_y = 0.0
            if -right_stick_deadzone_x < right_stick_x < right_stick_deadzone_x:
                right_stick_x = 0.0
            if -right_stick_deadzone_y < right_stick_y < right_stick_deadzone_y:
                right_stick_y = 0.0
            if left_trigger < left_trigger_deadzone: # This logic seems inverted from C, but matches behavior
                left_trigger = -1.0
            if right_trigger < right_trigger_deadzone: # This logic seems inverted from C, but matches behavior
                right_trigger = -1.0

            gamepad_name_lower = gamepad_name.lower() if gamepad_name else ""

            if XBOX_ALIAS_1 in gamepad_name_lower or XBOX_ALIAS_2 in gamepad_name_lower:
                rl.draw_texture(tex_xbox_pad, 0, 0, rl.DARKGRAY)

                # Draw buttons: xbox home
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE):
                    rl.draw_circle(394, 89, 19, rl.RED)

                # Draw buttons: basic
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE_RIGHT):
                    rl.draw_circle(436, 150, 9, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE_LEFT):
                    rl.draw_circle(352, 150, 9, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_LEFT):
                    rl.draw_circle(501, 151, 15, rl.BLUE)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN):
                    rl.draw_circle(536, 187, 15, rl.LIME)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_RIGHT):
                    rl.draw_circle(572, 151, 15, rl.MAROON)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_UP):
                    rl.draw_circle(536, 115, 15, rl.GOLD)

                # Draw buttons: d-pad
                rl.draw_rectangle(317, 202, 19, 71, rl.BLACK)
                rl.draw_rectangle(293, 228, 69, 19, rl.BLACK)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_UP):
                    rl.draw_rectangle(317, 202, 19, 26, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_DOWN):
                    rl.draw_rectangle(317, 202 + 45, 19, 26, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT):
                    rl.draw_rectangle(292, 228, 25, 19, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT):
                    rl.draw_rectangle(292 + 44, 228, 26, 19, rl.RED)

                # Draw buttons: left-right back
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_TRIGGER_1):
                    rl.draw_circle(259, 61, 20, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_TRIGGER_1):
                    rl.draw_circle(536, 61, 20, rl.RED)

                # Draw axis: left joystick
                left_gamepad_color = rl.RED if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_THUMB) else rl.BLACK
                rl.draw_circle(259, 152, 39, rl.BLACK)
                rl.draw_circle(259, 152, 34, rl.LIGHTGRAY)
                rl.draw_circle(int(259 + (left_stick_x * 20)),
                               int(152 + (left_stick_y * 20)), 25, left_gamepad_color)

                # Draw axis: right joystick
                right_gamepad_color = rl.RED if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_THUMB) else rl.BLACK
                rl.draw_circle(461, 237, 38, rl.BLACK)
                rl.draw_circle(461, 237, 33, rl.LIGHTGRAY)
                rl.draw_circle(int(461 + (right_stick_x * 20)),
                                int(237 + (right_stick_y * 20)), 25, right_gamepad_color)

                # Draw axis: left-right triggers
                rl.draw_rectangle(170, 30, 15, 70, rl.GRAY)
                rl.draw_rectangle(604, 30, 15, 70, rl.GRAY)
                rl.draw_rectangle(170, 30, 15, int(((1 + left_trigger) / 2) * 70), rl.RED)
                rl.draw_rectangle(604, 30, 15, int(((1 + right_trigger) / 2) * 70), rl.RED)

            elif PS_ALIAS in gamepad_name_lower:
                rl.draw_texture(tex_ps3_pad, 0, 0, rl.DARKGRAY)

                # Draw buttons: ps
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE):
                    rl.draw_circle(396, 222, 13, rl.RED)

                # Draw buttons: basic
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE_LEFT):
                    rl.draw_rectangle(328, 170, 32, 13, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE_RIGHT):
                    rl.draw_triangle(rl.Vector2(436, 168), rl.Vector2(436, 185), rl.Vector2(464, 177), rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_UP):
                    rl.draw_circle(557, 144, 13, rl.LIME)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_RIGHT):
                    rl.draw_circle(586, 173, 13, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN):
                    rl.draw_circle(557, 203, 13, rl.VIOLET)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_LEFT):
                    rl.draw_circle(527, 173, 13, rl.PINK)

                # Draw buttons: d-pad
                rl.draw_rectangle(225, 132, 24, 84, rl.BLACK)
                rl.draw_rectangle(195, 161, 84, 25, rl.BLACK)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_UP):
                    rl.draw_rectangle(225, 132, 24, 29, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_DOWN):
                    rl.draw_rectangle(225, 132 + 54, 24, 30, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT):
                    rl.draw_rectangle(195, 161, 30, 25, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT):
                    rl.draw_rectangle(195 + 54, 161, 30, 25, rl.RED)

                # Draw buttons: left-right back buttons
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_TRIGGER_1):
                    rl.draw_circle(239, 82, 20, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_TRIGGER_1):
                    rl.draw_circle(557, 82, 20, rl.RED)

                # Draw axis: left joystick
                left_gamepad_color = rl.RED if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_THUMB) else rl.BLACK
                rl.draw_circle(319, 255, 35, rl.BLACK)
                rl.draw_circle(319, 255, 31, rl.LIGHTGRAY)
                rl.draw_circle(int(319 + (left_stick_x * 20)),
                               int(255 + (left_stick_y * 20)), 25, left_gamepad_color)

                # Draw axis: right joystick
                right_gamepad_color = rl.RED if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_THUMB) else rl.BLACK
                rl.draw_circle(475, 255, 35, rl.BLACK)
                rl.draw_circle(475, 255, 31, rl.LIGHTGRAY)
                rl.draw_circle(int(475 + (right_stick_x * 20)),
                                int(255 + (right_stick_y * 20)), 25, right_gamepad_color)

                # Draw axis: left-right triggers
                rl.draw_rectangle(169, 48, 15, 70, rl.GRAY)
                rl.draw_rectangle(611, 48, 15, 70, rl.GRAY)
                rl.draw_rectangle(169, 48, 15, int(((1 + left_trigger) / 2) * 70), rl.RED)
                rl.draw_rectangle(611, 48, 15, int(((1 + right_trigger) / 2) * 70), rl.RED)
            else:
                # Draw background: generic
                rl.draw_rectangle_rounded(rl.Rectangle(175, 110, 460, 220), 0.3, 16, rl.DARKGRAY)

                # Draw buttons: basic
                rl.draw_circle(365, 170, 12, rl.RAYWHITE)
                rl.draw_circle(405, 170, 12, rl.RAYWHITE)
                rl.draw_circle(445, 170, 12, rl.RAYWHITE)
                rl.draw_circle(516, 191, 17, rl.RAYWHITE)
                rl.draw_circle(551, 227, 17, rl.RAYWHITE)
                rl.draw_circle(587, 191, 17, rl.RAYWHITE)
                rl.draw_circle(551, 155, 17, rl.RAYWHITE)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE_LEFT):
                    rl.draw_circle(365, 170, 10, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE):
                    rl.draw_circle(405, 170, 10, rl.GREEN)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_MIDDLE_RIGHT):
                    rl.draw_circle(445, 170, 10, rl.BLUE)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_LEFT):
                    rl.draw_circle(516, 191, 15, rl.GOLD)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN):
                    rl.draw_circle(551, 227, 15, rl.BLUE)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_RIGHT):
                    rl.draw_circle(587, 191, 15, rl.GREEN)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_UP):
                    rl.draw_circle(551, 155, 15, rl.RED)

                # Draw buttons: d-pad
                rl.draw_rectangle(245, 145, 28, 88, rl.RAYWHITE)
                rl.draw_rectangle(215, 174, 88, 29, rl.RAYWHITE)
                rl.draw_rectangle(247, 147, 24, 84, rl.BLACK)
                rl.draw_rectangle(217, 176, 84, 25, rl.BLACK)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_UP):
                    rl.draw_rectangle(247, 147, 24, 29, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_DOWN):
                    rl.draw_rectangle(247, 147 + 54, 24, 30, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT):
                    rl.draw_rectangle(217, 176, 30, 25, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT):
                    rl.draw_rectangle(217 + 54, 176, 30, 25, rl.RED)

                # Draw buttons: left-right back
                rl.draw_rectangle_rounded(rl.Rectangle(215, 98, 100, 10), 0.5, 16, rl.DARKGRAY)
                rl.draw_rectangle_rounded(rl.Rectangle(495, 98, 100, 10), 0.5, 16, rl.DARKGRAY)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_TRIGGER_1):
                    rl.draw_rectangle_rounded(rl.Rectangle(215, 98, 100, 10), 0.5, 16, rl.RED)
                if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_TRIGGER_1):
                    rl.draw_rectangle_rounded(rl.Rectangle(495, 98, 100, 10), 0.5, 16, rl.RED)

                # Draw axis: left joystick
                left_gamepad_color = rl.RED if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_LEFT_THUMB) else rl.BLACK
                rl.draw_circle(345, 260, 40, rl.BLACK)
                rl.draw_circle(345, 260, 35, rl.LIGHTGRAY)
                rl.draw_circle(int(345 + (left_stick_x * 20)),
                               int(260 + (left_stick_y * 20)), 25, left_gamepad_color)

                # Draw axis: right joystick
                right_gamepad_color = rl.RED if rl.is_gamepad_button_down(gamepad, rl.GamepadButton.GAMEPAD_BUTTON_RIGHT_THUMB) else rl.BLACK
                rl.draw_circle(465, 260, 40, rl.BLACK)
                rl.draw_circle(465, 260, 35, rl.LIGHTGRAY)
                rl.draw_circle(int(465 + (right_stick_x * 20)),
                                int(260 + (right_stick_y * 20)), 25, right_gamepad_color)

                # Draw axis: left-right triggers
                rl.draw_rectangle(151, 110, 15, 70, rl.GRAY)
                rl.draw_rectangle(644, 110, 15, 70, rl.GRAY)
                rl.draw_rectangle(151, 110, 15, int(((1 + left_trigger) / 2) * 70), rl.RED)
                rl.draw_rectangle(644, 110, 15, int(((1 + right_trigger) / 2) * 70), rl.RED)


            rl.draw_text(f"DETECTED AXIS [{rl.get_gamepad_axis_count(gamepad)}]:", 10, 50, 10, rl.MAROON)

            for i in range(rl.get_gamepad_axis_count(gamepad)):
                rl.draw_text(f"AXIS {i}: {rl.get_gamepad_axis_movement(gamepad, i):.02f}", 20, 70 + 20 * i, 10, rl.DARKGRAY)
            
            button_pressed = rl.get_gamepad_button_pressed()
            if button_pressed != rl.GamepadButton.GAMEPAD_BUTTON_UNKNOWN:
                rl.draw_text(f"DETECTED BUTTON: {button_pressed}", 10, 430, 10, rl.RED)
            else:
                rl.draw_text("DETECTED BUTTON: NONE", 10, 430, 10, rl.GRAY)
        else:
            rl.draw_text(f"GP{gamepad}: NOT DETECTED", 10, 10, 10, rl.GRAY)
            rl.draw_texture(tex_xbox_pad, 0, 0, rl.LIGHTGRAY)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.unload_texture(tex_ps3_pad)
    rl.unload_texture(tex_xbox_pad)

    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
