"""raylib [core] example - Input Gestures Detection
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.4, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2016-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

MAX_GESTURE_STRINGS = 20

def main():
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - input gestures")

    touch_position = rl.Vector2(0, 0)
    touch_area = rl.Rectangle(220, 10, screen_width - 230.0, screen_height - 20.0)

    gestures_count = 0
    gesture_strings = ["" for _ in range(MAX_GESTURE_STRINGS)]

    current_gesture = rl.Gesture.GESTURE_NONE
    last_gesture = rl.Gesture.GESTURE_NONE

    # rl.set_gestures_enabled(0b0000000000001001)  # Enable only some gestures to be detected

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        last_gesture = current_gesture
        current_gesture = rl.get_gesture_detected()
        touch_position = rl.get_touch_position(0)

        if rl.check_collision_point_rec(touch_position, touch_area) and (current_gesture != rl.Gesture.GESTURE_NONE):
            if current_gesture != last_gesture:
                # Store gesture string
                if current_gesture == rl.Gesture.GESTURE_TAP:
                    gesture_strings[gestures_count] = "GESTURE TAP"
                elif current_gesture == rl.Gesture.GESTURE_DOUBLETAP:
                    gesture_strings[gestures_count] = "GESTURE DOUBLETAP"
                elif current_gesture == rl.Gesture.GESTURE_HOLD:
                    gesture_strings[gestures_count] = "GESTURE HOLD"
                elif current_gesture == rl.Gesture.GESTURE_DRAG:
                    gesture_strings[gestures_count] = "GESTURE DRAG"
                elif current_gesture == rl.Gesture.GESTURE_SWIPE_RIGHT:
                    gesture_strings[gestures_count] = "GESTURE SWIPE RIGHT"
                elif current_gesture == rl.Gesture.GESTURE_SWIPE_LEFT:
                    gesture_strings[gestures_count] = "GESTURE SWIPE LEFT"
                elif current_gesture == rl.Gesture.GESTURE_SWIPE_UP:
                    gesture_strings[gestures_count] = "GESTURE SWIPE UP"
                elif current_gesture == rl.Gesture.GESTURE_SWIPE_DOWN:
                    gesture_strings[gestures_count] = "GESTURE SWIPE DOWN"
                elif current_gesture == rl.Gesture.GESTURE_PINCH_IN:
                    gesture_strings[gestures_count] = "GESTURE PINCH IN"
                elif current_gesture == rl.Gesture.GESTURE_PINCH_OUT:
                    gesture_strings[gestures_count] = "GESTURE PINCH OUT"

                gestures_count += 1

                # Reset gestures strings
                if gestures_count >= MAX_GESTURE_STRINGS:
                    gesture_strings = ["" for _ in range(MAX_GESTURE_STRINGS)]
                    gestures_count = 0
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()

        rl.clear_background(rl.RAYWHITE)

        rl.draw_rectangle_rec(touch_area, rl.GRAY)
        rl.draw_rectangle(225, 15, screen_width - 240, screen_height - 30, rl.RAYWHITE)

        rl.draw_text("GESTURES TEST AREA", screen_width - 270, screen_height - 40, 20, rl.fade(rl.GRAY, 0.5))

        for i in range(gestures_count):
            if i % 2 == 0:
                rl.draw_rectangle(10, 30 + 20 * i, 200, 20, rl.fade(rl.LIGHTGRAY, 0.5))
            else:
                rl.draw_rectangle(10, 30 + 20 * i, 200, 20, rl.fade(rl.LIGHTGRAY, 0.3))

            if i < gestures_count - 1:
                rl.draw_text(gesture_strings[i], 35, 36 + 20 * i, 10, rl.DARKGRAY)
            else:
                rl.draw_text(gesture_strings[i], 35, 36 + 20 * i, 10, rl.MAROON)

        rl.draw_rectangle_lines(10, 29, 200, screen_height - 50, rl.GRAY)
        rl.draw_text("DETECTED GESTURES", 50, 15, 10, rl.GRAY)

        if current_gesture != rl.Gesture.GESTURE_NONE:
            rl.draw_circle_v(touch_position, 30, rl.MAROON)

        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
