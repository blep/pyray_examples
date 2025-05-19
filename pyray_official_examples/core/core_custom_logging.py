"""raylib [core] example - Custom logging
Example complexity rating: [★★★☆] 3/4
Example originally created with raylib 2.5, last time updated with raylib 2.5
Example contributed by Pablo Marcos Oltra (@pamarcos) and reviewed by Ramon Santamaria (@raysan5)
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2018-2025 Pablo Marcos Oltra (@pamarcos) and Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
import time
from ctypes import CFUNCTYPE, c_int, c_char_p, c_void_p

# Custom logging function
# NOTE: This function is a C callback, so it needs to be defined with ctypes
@CFUNCTYPE(None, c_int, c_char_p, c_void_p)
def custom_log(msg_type, text, args):
    # Python's vprintf equivalent is not straightforward with ctypes' va_list.
    # For simplicity, we'll just print the text.
    # A more complete solution would involve parsing the format string and args,
    # but that's complex and often not necessary for basic logging.
    
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    type_str = ""
    if msg_type == rl.LOG_INFO:
        type_str = "[INFO] : "
    elif msg_type == rl.LOG_ERROR:
        type_str = "[ERROR]: "
    elif msg_type == rl.LOG_WARNING:
        type_str = "[WARN] : "
    elif msg_type == rl.LOG_DEBUG:
        type_str = "[DEBUG]: "
    
    # Decode bytes to string for printing
    try:
        decoded_text = text.decode('utf-8')
    except UnicodeDecodeError:
        decoded_text = str(text) # Fallback if decoding fails

    # The original C example uses vprintf(text, args) which handles format specifiers.
    # Python's print doesn't directly take a va_list.
    # We'll print the raw text. If format specifiers are present, they won't be processed.
    # For a more robust solution, one might need to inspect `args` if the C side
    # actually passes variable arguments that need formatting. However, raylib's
    # internal logging usually pre-formats the string before calling the callback.
    print(f"[{time_str}] {type_str}{decoded_text}")


def main():
    screen_width = 800
    screen_height = 450

    # Set custom logger
    rl.set_trace_log_callback(custom_log)

    rl.init_window(screen_width, screen_height, "raylib [core] example - custom logging")

    rl.set_target_fps(60)

    rl.trace_log(rl.LOG_INFO, "Custom logger initialized successfully")
    rl.trace_log(rl.LOG_WARNING, "This is a warning message")
    rl.trace_log(rl.LOG_ERROR, "This is an error message")
    rl.trace_log(rl.LOG_DEBUG, "This is a debug message")


    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        rl.draw_text("Check out the console output to see the custom logger in action!", 60, 200, 20, rl.LIGHTGRAY)
        rl.end_drawing()

    rl.close_window()

if __name__ == '__main__':
    main()
