"""raylib [core] example - custom frame control
Example complexity rating: [★★★★] 4/4
NOTE: WARNING: This is an example for advanced users willing to have full control over
the frame processes. By default, EndDrawing() calls the following processes:
    1. Draw remaining batch data: rlDrawRenderBatchActive()
    2. SwapScreenBuffer()
    3. Frame time control: WaitTime()
    4. PollInputEvents()
To avoid steps 2, 3 and 4, flag SUPPORT_CUSTOM_FRAME_CONTROL can be enabled in
config.h (it requires recompiling raylib). This way those steps are up to the user.
Note that enabling this flag invalidates some functions:
    - GetFrameTime()
    - SetTargetFPS()
    - GetFPS()
Example originally created with raylib 4.0, last time updated with raylib 4.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2021-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl

# Defines and Macros
MAX_FRAME_TIME_SAMPLES = 100

# Global Variables Definition
screen_width = 800
screen_height = 450

# Frame times tracking
frame_time_history = [0.0] * MAX_FRAME_TIME_SAMPLES
frame_time_counter = 0
average_frame_time = 0.0
max_frame_time = 0.0
min_frame_time = 0.0

pause = False

# For UpdateTimers state
_update_timers_index = 0
_update_timers_history_sum = 0.0

def update_my_logic():
    global pause
    if rl.is_key_pressed(rl.KEY_SPACE):
        pause = not pause

def draw_my_stuff():
    global average_frame_time, max_frame_time, min_frame_time, frame_time_counter, screen_width, screen_height, frame_time_history, pause

    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    if not pause:
        rl.draw_text("Custom frame control implemented!", 30, 20, 20, rl.MAROON)
        
        # rl.get_frame_time() when SetTargetFPS is not used (or 0) returns the previous frame time.
        # The C example doesn't set a target FPS in the custom loop, so GetFrameTime() is last frame's time.
        rl.draw_text(f"Target time per frame: {rl.get_frame_time()*1000.0:.03f} ms", 30, 50, 10, rl.DARKGRAY)

        current_frame_time_display_index = (frame_time_counter - 1 + MAX_FRAME_TIME_SAMPLES) % MAX_FRAME_TIME_SAMPLES if MAX_FRAME_TIME_SAMPLES > 0 else 0
        displayed_last_frame_time = frame_time_history[current_frame_time_display_index] if MAX_FRAME_TIME_SAMPLES > 0 else 0.0
        rl.draw_text(f"Frame time last frame: {displayed_last_frame_time:.03f} ms", 30, 80, 10, rl.DARKGRAY)
        rl.draw_text(f"Min frame time in history: {min_frame_time:.03f} ms", 30, 110, 10, rl.DARKGRAY)
        rl.draw_text(f"Max frame time in history: {max_frame_time:.03f} ms", 30, 140, 10, rl.DARKGRAY)
        rl.draw_text(f"Avg frame time in history: {average_frame_time:.03f} ms", 30, 170, 10, rl.DARKGRAY)

        rl.draw_text(f"TARGET FPS: {rl.get_target_fps()}", screen_width - 130, 20, 20, rl.LIME if rl.get_target_fps() > 0 else rl.GRAY)
        rl.draw_fps(screen_width - 100, 50)

        rl.draw_text("Press SPACE to PAUSE", 30, screen_height - 40, 20, rl.GRAY)
    else:
        text = "GAME PAUSED"
        text_width = rl.measure_text(text, 40)
        rl.draw_text(text, screen_width // 2 - text_width // 2, screen_height // 2 - 40, 40, rl.GRAY)

    rl.end_drawing()

def update_timers():
    global _update_timers_index, _update_timers_history_sum
    global min_frame_time, max_frame_time, average_frame_time, frame_time_history

    if MAX_FRAME_TIME_SAMPLES == 0: return

    current_sample_to_process_idx = _update_timers_index

    if _update_timers_index == 0: 
        min_frame_time = frame_time_history[current_sample_to_process_idx]
        max_frame_time = frame_time_history[current_sample_to_process_idx]
        _update_timers_history_sum = 0.0
    
    current_sample_value = frame_time_history[current_sample_to_process_idx]
    _update_timers_history_sum += current_sample_value
    if current_sample_value < min_frame_time:
        min_frame_time = current_sample_value
    if current_sample_value > max_frame_time:
        max_frame_time = current_sample_value

    _update_timers_index += 1

    if _update_timers_index >= MAX_FRAME_TIME_SAMPLES:
        average_frame_time = _update_timers_history_sum / MAX_FRAME_TIME_SAMPLES
        _update_timers_index = 0

def update_draw_frame(): # For emscripten_set_main_loop equivalence
    update_my_logic()
    draw_my_stuff()

def main():
    global screen_width, screen_height, frame_time_counter, frame_time_history, pause

    rl.init_window(screen_width, screen_height, "raylib [core] example - custom frame control")

    previous_time = rl.get_time()

    while not rl.window_should_close():
        current_time_start_frame = rl.get_time()
        update_draw_time = current_time_start_frame - previous_time # Total time for the previous frame
        # `previous_time` for the next iteration will be set after wait time.

        update_my_logic()
        draw_my_stuff()

        current_time_after_draw = rl.get_time()
        frame_time_current_processing = current_time_after_draw - current_time_start_frame
        
        last_frame_duration_for_wait = update_draw_time 
        
        if frame_time_current_processing < last_frame_duration_for_wait:
            rl.wait_time(last_frame_duration_for_wait - frame_time_current_processing)
        
        previous_time = rl.get_time() # Update previous_time to after the wait for the next iteration.

        update_timers() 

        if MAX_FRAME_TIME_SAMPLES > 0:
            frame_time_history[frame_time_counter] = float(update_draw_time * 1000.0) # in ms
            frame_time_counter = (frame_time_counter + 1) % MAX_FRAME_TIME_SAMPLES

    rl.close_window()

if __name__ == '__main__':
    main()
