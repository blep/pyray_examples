"""raylib [core] example - Windows drop files
Example complexity rating: [★★☆☆] 2/4
NOTE: This example only works on platforms that support drag & drop (Windows, Linux, OSX, Html5?)
Example originally created with raylib 1.3, last time updated with raylib 4.2
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2015-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

import pyray as rl
# from raylib.defines import MAX_FILEPATH_SIZE # Assuming this is defined in raylib.py or a similar place
MAX_FILEPATH_SIZE = 1024 # work-around

MAX_FILEPATH_RECORDED = 4096

def main():
    screen_width = 800
    screen_height = 450

    rl.init_window(screen_width, screen_height, "raylib [core] example - drop files")

    file_path_counter = 0
    # In Python, a list of strings is more natural.
    # We don't need to pre-allocate in the same way as C.
    file_paths = []

    rl.set_target_fps(60)

    while not rl.window_should_close():
        if rl.is_file_dropped():
            dropped_files = rl.load_dropped_files()

            for i in range(dropped_files.count):
                if file_path_counter < MAX_FILEPATH_RECORDED:
                    # Ensure the path is a Python string
                    path_str = dropped_files.paths[i].decode('utf-8') if isinstance(dropped_files.paths[i], bytes) else str(dropped_files.paths[i])
                    file_paths.append(path_str)
                    file_path_counter += 1
            
            rl.unload_dropped_files(dropped_files)

        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        if file_path_counter == 0:
            rl.draw_text("Drop your files to this window!", 100, 40, 20, rl.DARKGRAY)
        else:
            rl.draw_text("Dropped files:", 100, 40, 20, rl.DARKGRAY)

            for i in range(file_path_counter):
                if i % 2 == 0:
                    rl.draw_rectangle(0, 85 + 40 * i, screen_width, 40, rl.fade(rl.LIGHTGRAY, 0.5))
                else:
                    rl.draw_rectangle(0, 85 + 40 * i, screen_width, 40, rl.fade(rl.LIGHTGRAY, 0.3))
                
                rl.draw_text(file_paths[i], 120, 100 + 40 * i, 10, rl.GRAY)

            rl.draw_text("Drop new files...", 100, 110 + 40 * file_path_counter, 20, rl.DARKGRAY)

        rl.end_drawing()

    # No explicit de-allocation needed for the file_paths list in Python as it's garbage collected.
    rl.close_window()

if __name__ == '__main__':
    main()
