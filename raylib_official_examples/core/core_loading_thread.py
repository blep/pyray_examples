"""raylib [core] example - loading thread
Example complexity rating: [★★★☆] 3/4
NOTE: This example requires linking with pthreads library on MinGW, 
it can be accomplished passing -static parameter to compiler
Example originally created with raylib 2.5, last time updated with raylib 3.0
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import threading
import time

# Global variables for thread communication
data_loaded = False
data_progress = 0
lock = threading.Lock()

def load_data_thread():
    global data_loaded, data_progress

    print("Loading thread started...")
    time_counter = 0  # Time counted in ms
    start_time = time.time()

    # We simulate data loading with a time counter for 5 seconds
    while time_counter < 5000:
        current_time = (time.time() - start_time) * 1000  # Current time in ms
        time_counter = int(current_time)

        with lock:
            data_progress = time_counter // 10
        
        time.sleep(0.01) # Simulate work and allow other threads to run

    with lock:
        data_loaded = True
    print("Loading thread finished.")

class State:
    WAITING = 0
    LOADING = 1
    FINISHED = 2

def main():
    global data_loaded, data_progress
    # Initialization
    # --------------------------------------------------------------------------------------
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - loading thread")

    thread = None
    state = State.WAITING
    frames_counter = 0

    rl.set_target_fps(60)  # Set our game to run at 60 frames-per-second
    # --------------------------------------------------------------------------------------

    # Main game loop
    while not rl.window_should_close():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        if state == State.WAITING:
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                with lock:
                    data_loaded = False
                    data_progress = 0
                thread = threading.Thread(target=load_data_thread)
                thread.start()
                print("Loading thread created and started.")
                state = State.LOADING
        elif state == State.LOADING:
            frames_counter += 1
            with lock:
                current_data_loaded = data_loaded
            
            if current_data_loaded:
                frames_counter = 0
                if thread and thread.is_alive():
                    thread.join() # Wait for the thread to complete
                print("Loading thread joined successfully.")
                state = State.FINISHED
        elif state == State.FINISHED:
            if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):
                # Reset everything to launch again
                with lock:
                    data_loaded = False
                    data_progress = 0
                state = State.WAITING
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        if state == State.WAITING:
            rl.draw_text("PRESS ENTER to START LOADING DATA", 150, 170, 20, rl.DARKGRAY)
        elif state == State.LOADING:
            with lock:
                current_progress = data_progress
            rl.draw_rectangle(150, 200, current_progress, 60, rl.SKYBLUE)
            if (frames_counter // 15) % 2:
                rl.draw_text("LOADING DATA...", 240, 210, 40, rl.DARKBLUE)
        elif state == State.FINISHED:
            rl.draw_rectangle(150, 200, 500, 60, rl.LIME)
            rl.draw_text("DATA LOADED!", 250, 210, 40, rl.GREEN)

        rl.draw_rectangle_lines(150, 200, 500, 60, rl.DARKGRAY)
        rl.end_drawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # --------------------------------------------------------------------------------------
    # Ensure thread is joined if window is closed while loading
    if thread and thread.is_alive():
        # Signal the thread to stop if it's designed to check a flag
        # For this example, we'll just wait for it to finish its current task
        print("Window closing, joining loading thread...")
        thread.join()
        print("Loading thread joined before closing.")

    rl.close_window()  # Close window and OpenGL context
    # --------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
