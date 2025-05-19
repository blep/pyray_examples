"""raylib [core] example - Input Gestures for Web
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 4.6-dev, last time updated with raylib 4.6-dev
Example contributed by ubkp (@ubkp) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2023-2025 ubkp (@ubkp)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import math

# Global definitions and declarations
# Common variables definitions
screen_width = 800
screen_height = 450
message_position = rl.Vector2(160, 7)

# Last gesture variables definitions
last_gesture = 0
last_gesture_position = rl.Vector2(165, 130)

# Gesture log variables definitions and functions declarations
GESTURE_LOG_SIZE = 20
gesture_log = ["" for _ in range(GESTURE_LOG_SIZE)]
gesture_log_index = GESTURE_LOG_SIZE
previous_gesture = 0

def get_gesture_name(i):
    if i == 0: return "None"
    if i == 1: return "Tap"
    if i == 2: return "Double Tap"
    if i == 4: return "Hold"
    if i == 8: return "Drag"
    if i == 16: return "Swipe Right"
    if i == 32: return "Swipe Left"
    if i == 64: return "Swipe Up"
    if i == 128: return "Swipe Down"
    if i == 256: return "Pinch In"
    if i == 512: return "Pinch Out"
    return "Unknown"

def get_gesture_color(i):
    if i == 0: return rl.BLACK
    if i == 1: return rl.BLUE
    if i == 2: return rl.SKYBLUE
    if i == 4: return rl.BLACK
    if i == 8: return rl.LIME
    if i == 16: return rl.RED
    if i == 32: return rl.RED
    if i == 64: return rl.RED
    if i == 128: return rl.RED
    if i == 256: return rl.VIOLET
    if i == 512: return rl.ORANGE
    return rl.BLACK

log_mode = 1  # Log mode values: 0 shows repeated events; 1 hides repeated events; 2 shows repeated events but hide hold events; 3 hides repeated events and hide hold events
gesture_color = rl.Color(0, 0, 0, 255)
log_button1 = rl.Rectangle(53, 7, 48, 26)
log_button2 = rl.Rectangle(108, 7, 36, 26)
gesture_log_position = rl.Vector2(10, 10)

# Protractor variables definitions
angle_length = 90.0
current_angle_degrees = 0.0
final_vector = rl.Vector2(0.0, 0.0)
protractor_position = rl.Vector2(266.0, 315.0)

def update_web():
    global last_gesture, previous_gesture, gesture_color, gesture_log_index, log_mode, current_angle_degrees, final_vector
    # Handle common
    current_gesture = rl.get_gesture_detected()
    current_drag_degrees = rl.get_gesture_drag_angle()
    current_pitch_degrees = rl.get_gesture_pinch_angle()
    touch_count = rl.get_touch_point_count()

    # Handle last gesture
    if current_gesture != 0 and current_gesture != 4 and current_gesture != previous_gesture:
        last_gesture = current_gesture

    # Handle gesture log
    if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
        if rl.check_collision_point_rec(rl.get_mouse_position(), log_button1):
            if log_mode == 3: log_mode = 2
            elif log_mode == 2: log_mode = 3
            elif log_mode == 1: log_mode = 0
            else: log_mode = 1
        elif rl.check_collision_point_rec(rl.get_mouse_position(), log_button2):
            if log_mode == 3: log_mode = 1
            elif log_mode == 2: log_mode = 0
            elif log_mode == 1: log_mode = 3
            else: log_mode = 2
    
    fill_log = 0
    if current_gesture != 0:
        if log_mode == 3:
            if (current_gesture != 4 and current_gesture != previous_gesture) or current_gesture < 3:
                fill_log = 1
        elif log_mode == 2:
            if current_gesture != 4:
                fill_log = 1
        elif log_mode == 1:
            if current_gesture != previous_gesture:
                fill_log = 1
        else: # log_mode == 0
            fill_log = 1
    
    if fill_log:
        previous_gesture = current_gesture
        gesture_color = get_gesture_color(current_gesture)
        if gesture_log_index <= 0:
            gesture_log_index = GESTURE_LOG_SIZE
        gesture_log_index -= 1
        gesture_log[gesture_log_index] = get_gesture_name(current_gesture)

    # Handle protractor
    if current_gesture > 255:  # Pinch In and Pinch Out
        current_angle_degrees = current_pitch_degrees
    elif current_gesture > 15:  # Swipe Right, Swipe Left, Swipe Up and Swipe Down
        current_angle_degrees = current_drag_degrees
    elif current_gesture > 0:  # Tap, Doubletap, Hold and Grab
        current_angle_degrees = 0.0
    
    current_angle_radians = (current_angle_degrees + 90.0) * math.pi / 180
    final_vector = rl.Vector2(
        (angle_length * math.sin(current_angle_radians)) + protractor_position.x,
        (angle_length * math.cos(current_angle_radians)) + protractor_position.y
    )

    # Handle touch and mouse pointer points
    MAX_TOUCH_COUNT = 32
    touch_position = [rl.Vector2(0, 0) for _ in range(MAX_TOUCH_COUNT)]
    mouse_position = rl.Vector2(0,0)
    if current_gesture != rl.GESTURE_NONE:
        if touch_count != 0:
            for i in range(touch_count):
                touch_position[i] = rl.get_touch_position(i)
        else:
            mouse_position = rl.get_mouse_position()

    # Draw
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Draw common
    rl.draw_text("*", int(message_position.x + 5), int(message_position.y + 5), 10, rl.BLACK)
    rl.draw_text("Example optimized for Web/HTML5\non Smartphones with Touch Screen.", int(message_position.x + 15), int(message_position.y + 5), 10, rl.BLACK)
    rl.draw_text("*", int(message_position.x + 5), int(message_position.y + 35), 10, rl.BLACK)
    rl.draw_text("While running on Desktop Web Browsers,\ninspect and turn on Touch Emulation.", int(message_position.x + 15), int(message_position.y + 35), 10, rl.BLACK)

    # Draw last gesture
    rl.draw_text("Last gesture", int(last_gesture_position.x + 33), int(last_gesture_position.y - 47), 20, rl.BLACK)
    rl.draw_text("Swipe         Tap       Pinch  Touch", int(last_gesture_position.x + 17), int(last_gesture_position.y - 18), 10, rl.BLACK)
    rl.draw_rectangle(int(last_gesture_position.x + 20), int(last_gesture_position.y), 20, 20, rl.RED if last_gesture == rl.GESTURE_SWIPE_UP else rl.LIGHTGRAY)
    rl.draw_rectangle(int(last_gesture_position.x), int(last_gesture_position.y + 20), 20, 20, rl.RED if last_gesture == rl.GESTURE_SWIPE_LEFT else rl.LIGHTGRAY)
    rl.draw_rectangle(int(last_gesture_position.x + 40), int(last_gesture_position.y + 20), 20, 20, rl.RED if last_gesture == rl.GESTURE_SWIPE_RIGHT else rl.LIGHTGRAY)
    rl.draw_rectangle(int(last_gesture_position.x + 20), int(last_gesture_position.y + 40), 20, 20, rl.RED if last_gesture == rl.GESTURE_SWIPE_DOWN else rl.LIGHTGRAY)
    rl.draw_circle(int(last_gesture_position.x + 80), int(last_gesture_position.y + 16), 10, rl.BLUE if last_gesture == rl.GESTURE_TAP else rl.LIGHTGRAY)
    rl.draw_ring(rl.Vector2(last_gesture_position.x + 103, last_gesture_position.y + 16), 6.0, 11.0, 0.0, 360.0, 0, rl.LIME if last_gesture == rl.GESTURE_DRAG else rl.LIGHTGRAY)
    rl.draw_circle(int(last_gesture_position.x + 80), int(last_gesture_position.y + 43), 10, rl.SKYBLUE if last_gesture == rl.GESTURE_DOUBLETAP else rl.LIGHTGRAY)
    rl.draw_circle(int(last_gesture_position.x + 103), int(last_gesture_position.y + 43), 10, rl.SKYBLUE if last_gesture == rl.GESTURE_DOUBLETAP else rl.LIGHTGRAY)
    rl.draw_triangle(
        rl.Vector2(last_gesture_position.x + 122, last_gesture_position.y + 16),
        rl.Vector2(last_gesture_position.x + 137, last_gesture_position.y + 26),
        rl.Vector2(last_gesture_position.x + 137, last_gesture_position.y + 6),
        rl.ORANGE if last_gesture == rl.GESTURE_PINCH_OUT else rl.LIGHTGRAY
    )
    rl.draw_triangle(
        rl.Vector2(last_gesture_position.x + 147, last_gesture_position.y + 6),
        rl.Vector2(last_gesture_position.x + 147, last_gesture_position.y + 26),
        rl.Vector2(last_gesture_position.x + 162, last_gesture_position.y + 16),
        rl.ORANGE if last_gesture == rl.GESTURE_PINCH_OUT else rl.LIGHTGRAY
    )
    rl.draw_triangle(
        rl.Vector2(last_gesture_position.x + 125, last_gesture_position.y + 33),
        rl.Vector2(last_gesture_position.x + 125, last_gesture_position.y + 53),
        rl.Vector2(last_gesture_position.x + 140, last_gesture_position.y + 43),
        rl.VIOLET if last_gesture == rl.GESTURE_PINCH_IN else rl.LIGHTGRAY
    )
    rl.draw_triangle(
        rl.Vector2(last_gesture_position.x + 144, last_gesture_position.y + 43),
        rl.Vector2(last_gesture_position.x + 159, last_gesture_position.y + 53),
        rl.Vector2(last_gesture_position.x + 159, last_gesture_position.y + 33),
        rl.VIOLET if last_gesture == rl.GESTURE_PINCH_IN else rl.LIGHTGRAY
    )
    for i in range(4):
        rl.draw_circle(int(last_gesture_position.x + 180), int(last_gesture_position.y + 7 + i * 15), 5, gesture_color if touch_count > i else rl.LIGHTGRAY)

    # Draw gesture log
    rl.draw_text("Log", int(gesture_log_position.x), int(gesture_log_position.y), 20, rl.BLACK)
    for i, ii in enumerate((gesture_log_index + j) % GESTURE_LOG_SIZE for j in range(GESTURE_LOG_SIZE)):
        rl.draw_text(gesture_log[ii], int(gesture_log_position.x), int(gesture_log_position.y + 410 - i * 20), 20, gesture_color if i == 0 else rl.LIGHTGRAY)
    
    log_button1_color = rl.GRAY
    log_button2_color = rl.GRAY
    if log_mode == 3:
        log_button1_color = rl.MAROON
        log_button2_color = rl.MAROON
    elif log_mode == 2:
        log_button2_color = rl.MAROON
    elif log_mode == 1:
        log_button1_color = rl.MAROON
        
    rl.draw_rectangle_rec(log_button1, log_button1_color)
    rl.draw_text("Hide", int(log_button1.x + 7), int(log_button1.y + 3), 10, rl.WHITE)
    rl.draw_text("Repeat", int(log_button1.x + 7), int(log_button1.y + 13), 10, rl.WHITE)
    rl.draw_rectangle_rec(log_button2, log_button2_color)
    rl.draw_text("Hide", int(log_button1.x + 62), int(log_button1.y + 3), 10, rl.WHITE)
    rl.draw_text("Hold", int(log_button1.x + 62), int(log_button1.y + 13), 10, rl.WHITE)

    # Draw protractor
    rl.draw_text("Angle", int(protractor_position.x + 55), int(protractor_position.y + 76), 10, rl.BLACK)
    angle_string = f"{current_angle_degrees:.2f}" 
    rl.draw_text(angle_string, int(protractor_position.x + 55), int(protractor_position.y + 92), 20, gesture_color)
    rl.draw_circle(int(protractor_position.x), int(protractor_position.y), 80.0, rl.WHITE)
    rl.draw_line_ex(rl.Vector2(protractor_position.x - 90, protractor_position.y), rl.Vector2(protractor_position.x + 90, protractor_position.y), 3.0, rl.LIGHTGRAY)
    rl.draw_line_ex(rl.Vector2(protractor_position.x, protractor_position.y - 90), rl.Vector2(protractor_position.x, protractor_position.y + 90), 3.0, rl.LIGHTGRAY)
    rl.draw_line_ex(rl.Vector2(protractor_position.x - 80, protractor_position.y - 45), rl.Vector2(protractor_position.x + 80, protractor_position.y + 45), 3.0, rl.GREEN)
    rl.draw_line_ex(rl.Vector2(protractor_position.x - 80, protractor_position.y + 45), rl.Vector2(protractor_position.x + 80, protractor_position.y - 45), 3.0, rl.GREEN)
    rl.draw_text("0", int(protractor_position.x + 96), int(protractor_position.y - 9), 20, rl.BLACK)
    rl.draw_text("30", int(protractor_position.x + 74), int(protractor_position.y - 68), 20, rl.BLACK)
    rl.draw_text("90", int(protractor_position.x - 11), int(protractor_position.y - 110), 20, rl.BLACK)
    rl.draw_text("150", int(protractor_position.x - 100), int(protractor_position.y - 68), 20, rl.BLACK)
    rl.draw_text("180", int(protractor_position.x - 124), int(protractor_position.y - 9), 20, rl.BLACK)
    rl.draw_text("210", int(protractor_position.x - 100), int(protractor_position.y + 50), 20, rl.BLACK)
    rl.draw_text("270", int(protractor_position.x - 18), int(protractor_position.y + 92), 20, rl.BLACK)
    rl.draw_text("330", int(protractor_position.x + 72), int(protractor_position.y + 50), 20, rl.BLACK)
    if current_angle_degrees != 0.0:
        rl.draw_line_ex(protractor_position, final_vector, 3.0, gesture_color)

    # Draw touch and mouse pointer points
    if current_gesture != rl.GESTURE_NONE:
        if touch_count != 0:
            for i in range(touch_count):
                rl.draw_circle_v(touch_position[i], 50.0, rl.fade(gesture_color, 0.5))
                rl.draw_circle_v(touch_position[i], 5.0, gesture_color)
            if touch_count == 2:
                rl.draw_line_ex(touch_position[0], touch_position[1], 8 if current_gesture == rl.GESTURE_PINCH_OUT else 12, gesture_color) #GESTURE_PINCH_OUT is 512
        else:
            rl.draw_circle_v(mouse_position, 35.0, rl.fade(gesture_color, 0.5))
            rl.draw_circle_v(mouse_position, 5.0, gesture_color)
            
    rl.end_drawing()

def main():
    rl.init_window(screen_width, screen_height, "raylib [core] example - input gestures web")

    # rl.set_target_fps(60) # Not strictly necessary for web, but good practice

    # This is for web. For desktop, use a standard loop.
    # For web, emscripten_set_main_loop is called by raylib's web template.
    # We just need to ensure our update function is called.
    # In pyray, this is handled automatically if you use the standard loop.
    # However, for clarity with the C example, we'll show how it might look.
    # if rl.PLATFORM_WEB: # This constant doesn't exist directly in pyray, check via other means or assume web for this example
    #    pass # pyray handles the main loop for web

    while not rl.window_should_close():
        update_web()

    rl.close_window()

if __name__ == '__main__':
    main()
